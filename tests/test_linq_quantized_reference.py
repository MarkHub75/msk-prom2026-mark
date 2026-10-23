import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import numpy as np
from ml.linq.quantized_reference import QuantizedReferenceBackend


class ReusableGraphTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.scales, self.report = root / 'scales.json', root / 'compile.json'
        self.scales.write_text(json.dumps({'n_input:0': {'data_type': 'int8', 'data_scale': 2},
                                          'n_score:0': {'data_scale': .25}}))
        self.report.write_text(json.dumps({'compile_status': 'PASS',
            'inputs': [{'name': 'input', 'shape': [1, 1], 'dtype': 'float32'}],
            'outputs': [{'name': 'score', 'shape': [1, 1], 'dtype': 'float32'}]}))
        class Graph:
            calls = 0
            def get_inputs_anchors(self): return {'input': 'n_input'}
            def get_outputs_anchors(self): return {'score': 'n_score'}
            def gm(self, **values):
                self.calls += 1
                return values['input'] * 2
        self.graph = Graph()

    def test_load_once_multiple_calls_and_owned_outputs(self):
        graph = self.graph
        class Loader:
            count = 0
            @classmethod
            def load(cls, path): cls.count += 1; return cls()
            def as_torch_graph(self, batch_size): return graph
        with patch.dict('sys.modules', {'tpu_framework': types.SimpleNamespace(QuantizedModel=Loader)}):
            backend = QuantizedReferenceBackend('fixture', self.scales, self.report)
            first = backend.infer({'input': np.array([[.6]], np.float32)})
            second = backend.infer({'input': np.array([[.6]], np.float32)})
        self.assertEqual(Loader.count, 1)
        self.assertEqual(graph.calls, 2)
        self.assertEqual(first['score'].item(), .5)
        first['score'][0, 0] = 999
        self.assertEqual(second['score'].item(), .5)

    def test_bad_inputs_rejected_without_graph_execution(self):
        backend = QuantizedReferenceBackend('fixture', self.scales, self.report, graph=self.graph)
        for inputs in [{'wrong': np.zeros((1, 1), np.float32)},
                       {'input': np.full((1, 1), np.nan, np.float32)},
                       {'input': np.zeros((1, 1), np.float64)}]:
            with self.assertRaises(ValueError): backend.infer(inputs)
        self.assertEqual(self.graph.calls, 0)

    def test_output_shape_mismatch_rejected(self):
        backend = QuantizedReferenceBackend('fixture', self.scales, self.report, graph=self.graph)
        self.graph.gm = lambda **values: values['input'].repeat(1, 2)
        with self.assertRaises(ValueError): backend.infer({'input': np.zeros((1, 1), np.float32)})

    def test_output_names_never_inferred_from_shape(self):
        self.graph.get_outputs_anchors = lambda: {'wrong': 'n_score'}
        with self.assertRaises(ValueError):
            QuantizedReferenceBackend('fixture', self.scales, self.report, graph=self.graph)


if __name__ == '__main__': unittest.main()
