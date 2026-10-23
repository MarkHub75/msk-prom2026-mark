"""Reusable vendor hardware-aware CPU graph; explicitly NOT TPU execution."""
import json
from pathlib import Path
import numpy as np
from .simulate import quantize_input, dequantize_output


class QuantizedReferenceBackend:
    def __init__(self, quantized_path, scales_path, compile_report, *, threads=2, graph=None):
        if type(threads) is not int or not 1 <= threads <= 2:
            raise ValueError('CPU thread allocation must be 1..2')
        import torch
        self.torch = torch
        torch.set_num_threads(threads)
        self.scales = json.loads(Path(scales_path).read_text())
        self.report = json.loads(Path(compile_report).read_text())
        if self.report['compile_status'] != 'PASS':
            raise ValueError('successful compile report required')
        if graph is None:
            from tpu_framework import QuantizedModel
            graph = QuantizedModel.load(str(quantized_path)).as_torch_graph(batch_size=1)
        self.graph = graph
        self.input_anchors = graph.get_inputs_anchors()
        self.output_anchors = graph.get_outputs_anchors()
        self.input_specs = {x['name']: x for x in self.report['inputs']}
        self.output_specs = {x['name']: x for x in self.report['outputs']}
        self.output_map = self.report.get('output_name_map') or {k: k for k in self.output_specs}
        if (set(self.input_anchors) != set(self.input_specs) or
                set(self.output_anchors) != set(self.output_specs) or
                set(self.output_map.values()) != set(self.output_specs) or
                len(self.output_map) != len(self.output_specs)):
            raise ValueError('explicit graph/compile names differ')

    def infer(self, inputs):
        if set(inputs) != set(self.input_specs):
            raise ValueError('input tensor names differ')
        coded = {}
        for name, value in inputs.items():
            spec = self.input_specs[name]
            if (list(value.shape) != spec['shape'] or value.dtype != np.dtype(spec['dtype'])
                    or not np.isfinite(value).all()):
                raise ValueError('input spec mismatch')
            coded[name] = self.torch.from_numpy(quantize_input(value, self.scales[self.input_anchors[name] + ':0']))
        with self.torch.no_grad():
            raw = self.graph.gm(**coded)
        names = list(self.output_anchors)
        if isinstance(raw, dict):
            raw_outputs = raw
        elif isinstance(raw, (tuple, list)):
            if len(raw) != len(names): raise ValueError('output count differs')
            raw_outputs = dict(zip(names, raw))
        elif len(names) == 1:
            raw_outputs = {names[0]: raw}
        else:
            raise ValueError('multiple outputs need explicit mapped tensors')
        if set(raw_outputs) != set(names):
            raise ValueError('output names differ')
        outputs = {}
        for name, value in raw_outputs.items():
            value = dequantize_output(value.detach().cpu().numpy(), self.scales[self.output_anchors[name] + ':0'])
            spec = self.output_specs[name]
            if (list(value.shape) != spec['shape'] or value.dtype != np.dtype(spec['dtype'])
                    or not np.isfinite(value).all()):
                raise ValueError('output spec mismatch')
            outputs[name] = np.array(value, copy=True, order='C')
        return {source: outputs[conditioned] for source, conditioned in self.output_map.items()}
