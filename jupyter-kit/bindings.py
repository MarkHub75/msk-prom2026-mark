"""Bind ONLY the actual already-working organizer notebook API here.

This module deliberately performs no login, network request or import of an
unverified client. The working remote call has not been shared with the agent.
Do not paste passwords/tokens into this file or export notebook session objects.
"""
BINDING_READY = False


def make_runner(program_path, input_names, output_names):
    """Return callable(named_inputs)->named numeric outputs.

    Use the ACTUAL example.ipynb upload/load path for program_path. Keep existing
    authenticated client objects inside that notebook session; don't serialize
    them. Check the actual reply's status_code==0 and select exact numeric arrays.
    No tensor rename, reshape, dtype conversion or codec may be guessed.
    """
    raise NotImplementedError('Actual service import/call/result extraction snippet is required')
