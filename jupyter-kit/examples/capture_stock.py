"""Capture the existing stock call through its explicit user-provided wrapper.

No guessed client import, HTTP endpoint or result structure. Once the actual
notebook snippet is available, bind it in the live kernel, never its credentials.
"""
from ml.linq.notebook import capture_call, ExpectedClass


def capture_stock(invoke_existing, inputs, output_names, program_path, output_dir,
                  expected_class=None):
    return capture_call(
        invoke_existing, inputs=inputs, output_names=output_names,
        program_path=program_path, output_dir=output_dir, model_id='stock-resnet50',
        expected_class=expected_class, placement_attested=True,
    )

# invoke_existing(named_inputs) must wait for the ACTUAL supplied service reply,
# reject status_code != 0, and return only explicitly selected numeric arrays.
# The observed class257/0.39s confirms a user-reported stock run; do not substitute
# a cached result for a fresh capture call. Axis/offset come from the notebook.
