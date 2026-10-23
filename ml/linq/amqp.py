"""One-request AMQP transport bound explicitly to the organizer's notebook.

Requires EXACT tpu_pycloud_format==0.0.1. No replacement codec, guessed PyTask
kwargs, guessed routing, credentials, or automatic publish retry is provided.
"""
from __future__ import annotations

import argparse
from collections.abc import Mapping
import copy
from dataclasses import dataclass
import importlib
import importlib.metadata
import importlib.util
import os
import re
import json
import math
from pathlib import Path
from time import monotonic
from uuid import uuid4

import numpy as np

from .notebook import capture_call, _arrays, _file_hash, _name, _save_report

FORMAT_VERSION = "0.0.1"
_MAX_BYTES = 128 * 1024 * 1024


class AmqpError(RuntimeError):
    """Only stable codes and allowlisted numeric/UUID diagnostics are exposed."""
    def __init__(self, code, phase, *, exception_type=None, status_code=None):
        super().__init__(code)
        self.details = {"code": code, "phase": phase}
        if exception_type is not None:
            self.details["exception_type"] = exception_type
        if status_code is not None:
            self.details["status_code"] = status_code


@dataclass(repr=False)
class AmqpBinding:
    """User-owned actual-notebook bindings; never print this object/parameters.

    task_factory(request_id, reply_queue, inputs, program) -> official fmt.PyTask
    get_response_id(decoded_response, AMQP_properties) returns explicit ID. Other
    selectors take decoded response, returning numeric status and
    ONLY selected named numeric output arrays. No response structure is assumed.
    request exchange/routing and reply policy have no service-specific defaults.
    """
    parameters: object
    task_factory: object
    get_response_id: object
    get_status: object
    get_outputs: object
    output_names: object
    request_exchange: str
    request_routing_key: str
    reply_policy: str
    reply_setup: object = None  # (channel, generated_reply_queue, request_id)
    properties_factory: object = None  # (request_id, generated_reply_queue, program)
    program_file: object = None  # explicit LOCAL bytes corresponding to remote identifier
    format_source_manifest: object = None  # reviewed source-only official-format inventory
    reply_queue_factory: object = None  # explicit (request_id)->queue_name, or server-generated
    get_service_error: object = None  # optional explicit worker error selector, never public JSON
    reply_exclusive: bool = True  # generic policy; official notebook explicitly uses False


def _load_format(source_manifest=None):
    try:
        version = importlib.metadata.version("tpu_pycloud_format")
    except importlib.metadata.PackageNotFoundError:
        version = None
    except Exception as error:
        raise AmqpError("official_format_unavailable", "load_format", exception_type=type(error).__name__) from None
    if version is not None and version != FORMAT_VERSION:
        raise AmqpError("official_format_wrong_version", "load_format")
    if source_manifest is not None:
        try:
            audit = json.loads(Path(source_manifest).read_text(encoding="utf-8"))
            expected = {"__init__.py", "_io.py", "headers.py", "message_pb2.py", "message.proto"}
            if (audit.get("distribution") != "tpu_pycloud_format" or audit.get("version") != FORMAT_VERSION or
                    not isinstance(audit.get("files"), dict) or set(audit["files"]) != expected):
                raise ValueError("invalid source inventory")
            spec = importlib.util.find_spec("tpu_pycloud_format")
            if spec is None or not spec.origin:
                raise ValueError("official source module unavailable")
            directory = Path(spec.origin).resolve().parent
            if {str(path.relative_to(directory)) for path in directory.rglob("*.py")} != expected - {"message.proto"}:
                raise ValueError("unreviewed active Python source")
            for name, digest in audit["files"].items():
                path = (directory / name).resolve()
                if not path.is_relative_to(directory) or _file_hash(path) != digest:
                    raise ValueError("official source hash mismatch")
        except Exception as error:
            raise AmqpError("official_format_source_verification_failed", "load_format",
                            exception_type=type(error).__name__) from None
    elif version is None:
        raise AmqpError("official_format_missing", "load_format")
    try:
        fmt = importlib.import_module("tpu_pycloud_format")
    except Exception as error:
        raise AmqpError("official_format_unavailable", "load_format", exception_type=type(error).__name__) from None
    if (not isinstance(getattr(fmt, "PyTask", None), type) or
            not callable(getattr(fmt, "serialize", None)) or
            not callable(getattr(fmt, "deserialize", None))):
        raise AmqpError("official_format_api_mismatch", "load_format")
    return fmt


def _validate_binding(binding):
    if not isinstance(binding, AmqpBinding):
        if isinstance(binding, Mapping):
            try:
                binding = AmqpBinding(**binding)
            except Exception:
                raise AmqpError("invalid_binding", "validate_binding") from None
        else:
            raise AmqpError("invalid_binding", "validate_binding")
    if type(binding.reply_exclusive) is not bool:
        raise AmqpError("explicit_reply_exclusive_policy_required", "validate_binding")
    callbacks = (binding.task_factory, binding.get_response_id, binding.get_status, binding.get_outputs)
    if not all(callable(fn) for fn in callbacks):
        raise AmqpError("explicit_binding_callbacks_required", "validate_binding")
    if not isinstance(binding.request_exchange, str) or not isinstance(binding.request_routing_key, str):
        raise AmqpError("explicit_request_routing_required", "validate_binding")
    if binding.reply_policy == "default_exchange":
        if binding.reply_setup is not None:
            raise AmqpError("ambiguous_reply_policy", "validate_binding")
    elif binding.reply_policy == "custom_setup":
        if not callable(binding.reply_setup):
            raise AmqpError("explicit_reply_setup_required", "validate_binding")
    else:
        raise AmqpError("explicit_reply_policy_required", "validate_binding")
    if binding.reply_queue_factory is not None and not callable(binding.reply_queue_factory):
        raise AmqpError("invalid_reply_queue_factory", "validate_binding")
    if binding.get_service_error is not None and not callable(binding.get_service_error):
        raise AmqpError("invalid_service_error_selector", "validate_binding")
    if binding.properties_factory is not None and not callable(binding.properties_factory):
        raise AmqpError("invalid_properties_factory", "validate_binding")
    if not isinstance(binding.output_names, (tuple, list)) or not binding.output_names:
        raise AmqpError("explicit_output_names_required", "validate_binding")
    try:
        names = [_name(name) for name in binding.output_names]
    except Exception:
        raise AmqpError("invalid_output_names", "validate_binding") from None
    if len(set(names)) != len(names):
        raise AmqpError("duplicate_output_names", "validate_binding")
    return binding


def _connection_parameters(original, timeout, host, port):
    """Copy supplied credentials/TLS unchanged; enforce current loopback tunnel."""
    if host != "127.0.0.1" or port != 15672:
        raise AmqpError("loopback_tunnel_127_0_0_1_15672_required", "connection_parameters")
    try:
        params = copy.copy(original)
        params.host, params.port = host, port
        # One attempt; TCP/socket, connection stack and broker-blocked waits bounded.
        params.connection_attempts, params.retry_delay = 1, 0
        params.socket_timeout = min(5.0, timeout / 2)
        params.stack_timeout = timeout
        params.blocked_connection_timeout = min(5.0, timeout)
        return params
    except Exception as error:
        raise AmqpError("invalid_connection_parameters", "connection_parameters", exception_type=type(error).__name__) from None


def _service_error_excerpt(value, parameters):
    """Allow only bounded sanitized worker error text, never worker metadata."""
    if not isinstance(value, str):
        return None
    # Explicitly supplied credentials only; no environment/store inspection here.
    credentials = getattr(parameters, "credentials", None)
    secrets = (getattr(credentials, "password", None),
               getattr(credentials, "username", None), os.environ.get("LINQ_LOGIN"))
    for secret in secrets:
        if isinstance(secret, str) and secret:
            value = value.replace(secret, "[redacted]")
    value = re.sub(r"(?i)([a-z][a-z0-9+.-]*://)[^/\s@]+@", r"\1[redacted]@", value)
    value = re.sub(r"(?i)(password|passwd|token|secret|authorization|cookie|api[_-]?key)(\s*[:=]\s*)([^&\s;]+)",
                   lambda match: match[1] + match[2] + "[redacted]", value)
    return value[:1024]


class AmqpRunner:
    """Blocking one-request callable with one explicitly configured response queue.

    A local timeout/publish failure leaves remote completion unknown. This runner
    never retries a publish and must not be blindly recalled as an automatic retry.
    Closed connections do NOT prove that remotely accepted execution was cancelled.
    """
    def __init__(self, binding, program, *, timeout=30.0, host="127.0.0.1", port=15672):
        if (not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or
                not math.isfinite(timeout) or timeout <= 0):
            raise AmqpError("positive_finite_timeout_required", "configuration")
        if not isinstance(program, str) or not program:
            raise AmqpError("explicit_program_identifier_required", "configuration")
        self.binding = _validate_binding(binding)
        self.program, self.timeout, self.host, self.port = program, float(timeout), host, port
        self.last_response = None
        self._private_service_error = None

    def __call__(self, inputs):
        started = monotonic()
        deadline = started + self.timeout
        request_id = str(uuid4())
        summary = {"request_id": request_id, "status": "not_started", "status_code": None,
                   "publish_attempted": False, "publish_confirmed": False,
                   "remote_completion": "not_submitted", "required_format_version": FORMAT_VERSION,
                   "timings": {}, "outputs": {}}
        self.last_response = summary
        connection = None
        phase = "validate_inputs"
        try:
            arrays = _arrays(inputs, max_bytes=_MAX_BYTES)
            phase = "load_format"
            fmt = _load_format(self.binding.format_source_manifest)  # Before any broker connection.
            phase = "load_pika"
            pika = importlib.import_module("pika")
            phase = "connection_parameters"
            parameters = _connection_parameters(self.binding.parameters, self.timeout, self.host, self.port)
            phase = "open_connection"
            connection = pika.BlockingConnection(parameters)
            phase = "open_channel"
            channel = connection.channel()
            # Standard AMQP queue semantics, selected explicitly by this transport.
            requested_queue = ("" if self.binding.reply_queue_factory is None else
                               self.binding.reply_queue_factory(request_id))
            if not isinstance(requested_queue, str):
                raise AmqpError("invalid_reply_queue_name", "declare_reply_queue")
            declared = channel.queue_declare(queue=requested_queue, durable=False, exclusive=self.binding.reply_exclusive, auto_delete=True)
            reply_queue = declared.method.queue
            if not isinstance(reply_queue, str) or not reply_queue:
                raise AmqpError("invalid_reply_queue", "declare_reply_queue")
            phase = "reply_setup"
            if self.binding.reply_policy == "custom_setup":
                self.binding.reply_setup(channel, reply_queue, request_id)
            phase = "build_task"
            task = self.binding.task_factory(request_id, reply_queue, arrays, self.program)
            if not isinstance(task, fmt.PyTask):
                raise AmqpError("task_factory_must_return_official_pytask", phase)
            phase = "serialize_request"
            body = fmt.serialize(task)
            if not isinstance(body, (bytes, bytearray)) or len(body) > _MAX_BYTES:
                raise AmqpError("invalid_serialized_request", phase)
            phase = "publish_properties"
            if self.binding.properties_factory is None:
                properties = pika.BasicProperties(correlation_id=request_id, reply_to=reply_queue)
            else:
                properties = self.binding.properties_factory(request_id, reply_queue, self.program)
            phase = "confirm_mode"
            channel.confirm_delivery()
            if monotonic() >= deadline:
                raise AmqpError("deadline_before_publish", phase)
            phase = "publish"
            summary.update(status="pending_response", publish_attempted=True, remote_completion="unknown")
            # Exactly one attempt, with mandatory routing and publisher confirmation.
            confirmed = channel.basic_publish(exchange=self.binding.request_exchange,
                routing_key=self.binding.request_routing_key, body=bytes(body),
                properties=properties, mandatory=True)
            if confirmed is False:
                raise AmqpError("publish_not_confirmed", phase)
            summary["publish_confirmed"] = True
            phase = "wait_response"
            while True:
                remaining = deadline - monotonic()
                if remaining <= 0:
                    raise AmqpError("response_timeout", phase)
                method, response_properties, response_body = channel.basic_get(queue=reply_queue, auto_ack=False)
                if method is None:
                    connection.process_data_events(time_limit=min(0.05, remaining))
                    continue
                phase = "deserialize_response"
                if not isinstance(response_body, (bytes, bytearray)) or len(response_body) > _MAX_BYTES:
                    raise AmqpError("invalid_serialized_response", phase)
                response = fmt.deserialize(bytes(response_body))
                phase = "correlate_response"
                if self.binding.get_response_id(response, response_properties) != request_id:
                    raise AmqpError("response_id_mismatch", phase)
                phase = "check_status"
                status = self.binding.get_status(response)
                if not isinstance(status, (int, np.integer)) or isinstance(status, (bool, np.bool_)):
                    raise AmqpError("numeric_status_required", phase)
                summary["status_code"] = int(status)
                summary["remote_completion"] = "response_received"
                if int(status) != 0:
                    if self.binding.get_service_error is not None:
                        private_error = self.binding.get_service_error(response)
                        if isinstance(private_error, str):
                            self._private_service_error = _service_error_excerpt(private_error, self.binding.parameters)
                            summary["service_error"] = self._private_service_error
                    channel.basic_ack(delivery_tag=method.delivery_tag)
                    raise AmqpError("service_reported_failure", phase, status_code=int(status))
                phase = "validate_outputs"
                outputs = _arrays(self.binding.get_outputs(response), names=self.binding.output_names,
                                  max_bytes=_MAX_BYTES)
                channel.basic_ack(delivery_tag=method.delivery_tag)
                summary.update(status="completed", remote_completion="response_received")
                summary["outputs"] = {name: {"shape": list(value.shape), "dtype": value.dtype.name}
                                      for name, value in outputs.items()}
                return outputs
        except AmqpError as error:
            summary.update(status="failed", error=dict(error.details))
            if error.details["code"].startswith("official_format_"):
                summary["next_action"] = "provide_exact_official_tpu_pycloud_format_0_0_1"
            raise
        except Exception as error:
            safe = AmqpError("transport_or_binding_failure", phase, exception_type=type(error).__name__)
            summary.update(status="failed", error=dict(safe.details))
            raise safe from None
        finally:
            if connection is not None:
                try:
                    connection.close()
                except Exception as error:
                    summary["close_error_type"] = type(error).__name__
            summary["timings"]["total_ms"] = (monotonic() - started) * 1000


def official_binding(parameters, *, request_exchange, request_routing_key, reply_exchange,
                     output_names, format_source_manifest=None, program_file=None, reply_queue_factory=None):
    """Use the INSPECTED official format; routing/URI/credentials stay explicit.

    PyTask(data=inputs) is the actual exported dataclass. deserialize returns
    (data, metadata, worker_data). IDs/URI/reply routing are official AMQP headers,
    not invented PyTask fields. No worker error string/metadata is exported.
    The worker's reply exchange must be supplied from the actual deployment.
    """
    fmt = _load_format(format_source_manifest)
    names = ("MESSAGE_ID_ATTR_NAME", "RESPONSE_ROUTING_KEYS_ATTR_NAME", "TARGET_URI_ATTR_NAME")
    if tuple(getattr(fmt, name, None) for name in names) != (
            "tpu_pycloud_message_id", "response_routing_keys", "uri"):
        raise AmqpError("official_header_constants_mismatch", "create_official_binding")
    if not isinstance(reply_exchange, str):
        raise AmqpError("explicit_reply_exchange_required", "create_official_binding")
    def task_factory(request_id, reply_queue, inputs, program):
        return fmt.PyTask(data=inputs)
    def properties_factory(request_id, reply_queue, program):
        pika = importlib.import_module("pika")
        return pika.BasicProperties(headers={fmt.MESSAGE_ID_ATTR_NAME: request_id,
            fmt.RESPONSE_ROUTING_KEYS_ATTR_NAME: json.dumps([reply_queue]),
            fmt.TARGET_URI_ATTR_NAME: program})
    def response_id(response, properties):
        headers = getattr(properties, "headers", None)
        return headers.get(fmt.MESSAGE_ID_ATTR_NAME) if isinstance(headers, Mapping) else None
    def checked_response(response):
        if not isinstance(response, tuple) or len(response) != 3 or not isinstance(response[2], Mapping):
            raise AmqpError("official_response_tuple_required", "select_response")
        return response
    def status(response):
        return checked_response(response)[2]["status_code"]
    def service_error(response):
        return checked_response(response)[2].get("error_message", "")
    def outputs(response):
        data = checked_response(response)[0]
        if not isinstance(data, Mapping):
            raise AmqpError("numeric_response_mapping_required", "select_outputs")
        return {name: data[name] for name in output_names}
    def reply_setup(channel, queue, request_id):
        channel.queue_bind(queue=queue, exchange=reply_exchange, routing_key=queue)
    return AmqpBinding(parameters=parameters, task_factory=task_factory,
        get_response_id=response_id, get_status=status, get_outputs=outputs,
        output_names=output_names, request_exchange=request_exchange,
        request_routing_key=request_routing_key,
        reply_policy="default_exchange" if reply_exchange == "" else "custom_setup",
        reply_setup=None if reply_exchange == "" else reply_setup,
        properties_factory=properties_factory, program_file=program_file,
        format_source_manifest=format_source_manifest, reply_queue_factory=reply_queue_factory,
        get_service_error=service_error, reply_exclusive=False)


def _environment_parameters(config_path=None):
    # Read only an explicitly selected file OR these three documented env keys.
    if config_path is not None:
        try:
            path = Path(config_path)
            if path.stat().st_size > 65536:
                raise ValueError("config too large")
            config = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(config, dict) or set(config) != {"username", "password", "virtual_host"}:
                raise ValueError("invalid config keys")
            username, password, vhost = (config["username"], config["password"], config["virtual_host"])
        except Exception as error:
            raise AmqpError("connection_config_invalid", "configuration", exception_type=type(error).__name__) from None
    else:
        username = os.environ.get("LINQ_AMQP_USERNAME")
        password = os.environ.get("LINQ_AMQP_PASSWORD")
        vhost = os.environ.get("LINQ_AMQP_VHOST")
    if not all(isinstance(value, str) and value for value in (username, password, vhost)):
        raise AmqpError("explicit_broker_credentials_and_vhost_required", "configuration")
    pika = importlib.import_module("pika")
    return pika.ConnectionParameters(host="127.0.0.1", port=15672, virtual_host=vhost,
                                     credentials=pika.PlainCredentials(username, password))


def _load_binding(value):
    try:
        module, name = value.split(":", 1)
        factory = getattr(importlib.import_module(module), name)
        return _validate_binding(factory())
    except AmqpError:
        raise
    except Exception as error:
        raise AmqpError("binding_load_failed", "load_binding", exception_type=type(error).__name__) from None


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise AmqpError("invalid_cli_arguments", "arguments")


def main(argv=None):
    parser = _Parser(description=__doc__)
    parser.add_argument("--binding", help="Optional trusted user-owned module:function returning AmqpBinding")
    parser.add_argument("--format-source-manifest", help="Reviewed source-only official 0.0.1 inventory")
    parser.add_argument("--exchange", help="Actual request exchange; explicitly pass empty string for default exchange")
    parser.add_argument("--routing-key", help="Actual worker request routing key")
    parser.add_argument("--reply-exchange", help="Actual worker reply exchange; explicitly pass empty string for default exchange")
    parser.add_argument("--output-name", action="append", help="Exact numeric response name; repeat for multiple outputs")
    parser.add_argument("--connection-config", help="Explicit private outside-Git JSON: username/password/virtual_host")
    parser.add_argument("--program", "--target-uri", dest="program", help="Exact actual program URI passed verbatim as official uri header")
    parser.add_argument("--login-env", help="Explicit env key containing actual LinQ login for the USER-CONFIRMED stock ResNet URI only")
    parser.add_argument("--notebook-reply-queue", action="store_true", help="Use actual notebook_{request_id[:8]} reply queue")
    parser.add_argument("--save-service-error", action="store_true", help="Preserve bounded worker error text privately outside Git; never stdout")
    parser.add_argument("--program-file", help="Local .tpu bytes for hash; not proof of loaded remote identity")
    parser.add_argument("--input-npz", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model-id", default="explicit-amqp-model")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=15672)
    parser.add_argument("--attest-program-match", action="store_true")
    parser.add_argument("--attest-linq-placement", action="store_true")
    runner = None
    try:
        args = parser.parse_args(argv)
        if args.program is not None and args.login_env is not None:
            raise AmqpError("choose_exact_uri_or_explicit_login_env", "configuration")
        if args.program is None:
            if args.login_env is None:
                raise AmqpError("explicit_target_uri_required", "configuration")
            login = os.environ.get(args.login_env)
            if not isinstance(login, str) or not login or any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-" for char in login):
                raise AmqpError("valid_explicit_linq_login_required", "configuration")
            # This path was explicitly supplied and confirmed by the user, not inferred.
            args.program = "file:///auto/cache/" + login + "/torch_resnet50_b1_o5_h1m.tpu?raw=False"
        # Useful action error before importing user binding/network dependencies.
        _load_format(args.format_source_manifest)
        if args.binding:
            binding = _load_binding(args.binding)
            if args.format_source_manifest is not None:
                binding.format_source_manifest = args.format_source_manifest
        else:
            if any(value is None for value in (args.exchange, args.routing_key, args.reply_exchange)) or not args.output_name:
                raise AmqpError("explicit_routing_reply_exchange_and_outputs_required", "configuration")
            binding = official_binding(_environment_parameters(args.connection_config),
                request_exchange=args.exchange, request_routing_key=args.routing_key,
                reply_exchange=args.reply_exchange, output_names=args.output_name,
                format_source_manifest=args.format_source_manifest, program_file=args.program_file,
                reply_queue_factory=(lambda request_id: "notebook_" + request_id[:8]) if args.notebook_reply_queue else None)
        local_program = args.program_file or binding.program_file
        if local_program is None:
            raise AmqpError("explicit_local_program_file_required", "configuration")
        with np.load(args.input_npz, allow_pickle=False) as archive:
            if len(set(archive.files)) != len(archive.files):
                raise AmqpError("duplicate_input_name", "load_inputs")
            inputs = _arrays({name: archive[name] for name in archive.files}, max_bytes=_MAX_BYTES)
        runner = AmqpRunner(binding, args.program, timeout=args.timeout, host=args.host, port=args.port)
        capture = capture_call(runner, inputs=inputs, output_names=list(binding.output_names),
            program_path=local_program, output_dir=args.output_dir, model_id=args.model_id,
            placement_attested=args.attest_linq_placement)
        capture["program_identity"] = {"hash_basis": "provided_local_file",
            "remote_program_match_attested": args.attest_program_match,
            "independently_verified": False}
        directory = Path(args.output_dir)
        path = directory / "capture.json"
        if path.is_file():
            # Never modify a preexisting capture rejected by capture_call.
            stored = json.loads(path.read_text())
            if stored.get("capture_id") == capture["capture_id"]:
                _save_report(path, capture)
                if runner.last_response is not None:
                    _save_report(directory / "response.json", runner.last_response)
                    if args.save_service_error and runner._private_service_error is not None:
                        fd = os.open(directory / "service-error.txt", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                        with os.fdopen(fd, "w", encoding="utf-8") as error_file:
                            error_file.write(runner._private_service_error)
        print(json.dumps({"status": capture["status"], "call_completed": capture["call_completed"],
                          "response": runner.last_response}, allow_nan=False))
        return 0 if capture["status"] == "completed" else 1
    except AmqpError as error:
        value = {"status": "failed", "error": error.details}
        if error.details["code"].startswith("official_format_"):
            value.update(required_format_version=FORMAT_VERSION,
                         next_action="provide_exact_official_tpu_pycloud_format_0_0_1")
        print(json.dumps(value))
        return 1
    except Exception as error:
        print(json.dumps({"status": "failed", "error": {
            "code": "cli_failure", "exception_type": type(error).__name__}}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
