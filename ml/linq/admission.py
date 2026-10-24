"""One local Matvey admission fence across all AMQP journal directories."""
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
from .journal import RequestJournal, TERMINAL, atomic_json, fsync_directory
from .namespace import canonical_id

DEFAULT_ADMISSION_DIR = '/workspace/artifacts/linq-rpc/matvey-admission'


class AdmissionError(RuntimeError):
    pass


class MatveyAdmission:
    def __init__(self, directory):
        self.directory = Path(directory).absolute()
        self.pointer = self.directory / 'active.json'
        self.locked = False

    def _load(self):
        if self.pointer.is_symlink(): raise AdmissionError('matvey_admission_invalid')
        if not self.pointer.exists(): return None
        try:
            value = json.loads(self.pointer.read_text())
            if set(value) != {'schema_version', 'request_id', 'journal_path'} or value['schema_version'] != '1.0':
                raise ValueError('invalid pointer')
            request_id = canonical_id(value['request_id'])
            path = Path(value['journal_path'])
            if (not path.is_absolute() or path != path.resolve() or path.name != 'request.json'
                    or path.parent.name != request_id): raise ValueError('invalid journal path')
            return value
        except (OSError, ValueError, TypeError, KeyError):
            raise AdmissionError('matvey_admission_invalid') from None

    def _safe(self, pointer):
        """Only proof of durable non-submission or correlated saved response releases."""
        store = RequestJournal(Path(pointer['journal_path']).parent.parent)
        request_id = pointer['request_id']
        try:
            with store.lock(request_id):
                record = store.load(request_id)
                if record['state'] not in TERMINAL | {'NOT_SUBMITTED'}: return False
                paths = [Path(pointer['journal_path'])]
                if record['state'] in TERMINAL:
                    status = record.get('status_code')
                    if (record.get('response_id') != request_id or type(status) is not int or
                            (record['state'] == 'COMPLETED') != (status == 0)): return False
                    outputs = store.outputs(request_id)  # checks numeric bytes/hashes
                    if status == 0 and set(outputs) != set(record['output_names']): return False
                    paths.append(store.path(request_id) / 'response.npz')
                for path in paths:
                    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
                    try: os.fsync(fd)
                    finally: os.close(fd)
                fsync_directory(store.path(request_id))
                return True
        except (OSError, ValueError, KeyError, TypeError):
            return False

    def _clear_safe(self, pointer):
        if not self._safe(pointer): return False
        self.pointer.unlink()
        fsync_directory(self.directory)
        return True

    @contextmanager
    def session(self, *, request_id=None, journal=None):
        if self.directory.is_symlink(): raise AdmissionError('matvey_admission_invalid')
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        fsync_directory(self.directory.parent)
        fd = os.open(self.directory / '.lock', os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        acquired = False
        try:
            try: fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError: raise AdmissionError('matvey_admission_busy') from None
            self.locked = True
            acquired = True
            active = self._load()
            if active is not None:
                same = (request_id == active['request_id'] and journal is not None and
                        str(journal.path(request_id) / 'request.json') == active['journal_path'])
                if not same and not self._clear_safe(active):
                    raise AdmissionError('matvey_pending_request_requires_reconcile')
            yield self
        finally:
            if acquired:
                try:
                    active = self._load()
                    if active is not None: self._clear_safe(active)
                except (OSError, AdmissionError):
                    pass  # failed durability proof retains the fence; never guess stale
                self.locked = False
            os.close(fd)  # lock file stays; OS releases only this process's flock

    def claim(self, journal, request_id):
        if not self.locked: raise AdmissionError('matvey_admission_lock_required')
        canonical_id(request_id)
        value = {'schema_version': '1.0', 'request_id': request_id,
                 'journal_path': str(journal.path(request_id) / 'request.json')}
        active = self._load()
        if active is not None and active != value:
            raise AdmissionError('matvey_pending_request_requires_reconcile')
        if active is None: atomic_json(self.pointer, value)
