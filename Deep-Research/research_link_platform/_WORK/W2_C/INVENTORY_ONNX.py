"""Read-only ONNX inventory for a future exact candidate; requires onnx + numpy.
No SDK imports, model execution, simplification or model rewriting.
Usage: python INVENTORY_ONNX.py candidate.onnx --out INVENTORY.json
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path


def main():
    import onnx
    from onnx import numpy_helper
    import numpy as np

    parser = argparse.ArgumentParser()
    parser.add_argument("model", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    # Avoid loading potentially huge external weight files just for graph inspection.
    model = onnx.load(str(args.model), load_external_data=False)

    def tensor(t):
        result = {"name": t.name, "dtype": t.data_type, "dims": list(t.dims),
                  "data_location": t.data_location,
                  "external_data": {x.key: x.value for x in t.external_data},
                  "proto_sha256": hashlib.sha256(t.SerializeToString()).hexdigest()}
        if t.data_location != onnx.TensorProto.EXTERNAL and np.prod(t.dims, dtype=np.int64) <= 64:
            try:
                result["small_values"] = numpy_helper.to_array(t).tolist()
            except Exception as exc:
                result["value_error"] = str(exc)
        return result

    def attribute(a):
        if a.type == onnx.AttributeProto.TENSOR:
            return tensor(a.t)
        if a.type == onnx.AttributeProto.GRAPH:
            return graph(a.g)
        if a.type == onnx.AttributeProto.GRAPHS:
            return [graph(g) for g in a.graphs]
        value = onnx.helper.get_attribute_value(a)
        if isinstance(value, bytes):
            return value.decode("utf8", errors="backslashreplace")
        if isinstance(value, (str, int, float)):
            return value
        if isinstance(value, (list, tuple)):
            return [x.decode("utf8", errors="backslashreplace") if isinstance(x, bytes) else x for x in value]
        return str(value)

    def info(v):
        return {"name": v.name, "type": str(v.type)}

    def graph(g):
        return {"name": g.name, "inputs": [info(v) for v in g.input],
                "outputs": [info(v) for v in g.output],
                "value_info": [info(v) for v in g.value_info],
                "initializers": [tensor(t) for t in g.initializer],
                "sparse_initializer_count": len(g.sparse_initializer),
                "operator_counts": dict(collections.Counter((n.domain + "::" + n.op_type) for n in g.node)),
                "nodes": [{"index": i, "name": n.name, "domain": n.domain,
                           "op_type": n.op_type, "inputs": list(n.input), "outputs": list(n.output),
                           "attributes": {a.name: attribute(a) for a in n.attribute}} for i, n in enumerate(g.node)]}

    result = {"file": str(args.model.resolve()), "file_sha256": hashlib.sha256(args.model.read_bytes()).hexdigest(),
              "onnx_package": onnx.__version__, "ir_version": model.ir_version,
              "opset_import": [{"domain": o.domain, "version": o.version} for o in model.opset_import],
              "producer_name": model.producer_name, "producer_version": model.producer_version,
              "metadata": {x.key: x.value for x in model.metadata_props},
              "local_function_count": len(model.functions), "graph": graph(model.graph),
              "validation": "Inventory only; no checker, shape inference, ORT, SDK or device run"}
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")


if __name__ == "__main__":
    main()
