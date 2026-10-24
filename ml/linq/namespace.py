"""Pure local guards for the user-authorized Matvey remote namespace."""
import re
from urllib.parse import urlsplit
from uuid import UUID


def canonical_id(value):
    if not isinstance(value, str) or str(UUID(value)) != value:
        raise ValueError('canonical request UUID required')
    return value


def reply_queue(request_id):
    return 'matvey_reply_' + canonical_id(request_id)


def check_reply_queue(value, request_id, *, legacy_request_ids=()):
    canonical_id(request_id)
    if value == reply_queue(request_id):
        return value
    if request_id in legacy_request_ids and value == 'notebook_' + request_id[:8]:
        return value
    raise ValueError('reply queue outside reviewed own request namespace')


def check_upload_queue(value):
    if not isinstance(value, str) or not value.startswith('matvey_upload_'):
        raise ValueError('owned upload queue required')
    canonical_id(value[len('matvey_upload_'):])
    return value


def check_program_name(name):
    if (not isinstance(name, str) or not re.fullmatch(r'matvey_[A-Za-z0-9][A-Za-z0-9_.-]*\.tpu', name)
            or '..' in name or 'mosprom_' in name or '_cut_ap9999' in name):
        raise ValueError('owned nonprotected program filename required')
    return name


def check_login(login):
    if (not isinstance(login, str) or not re.fullmatch(r'[A-Za-z0-9_@+-][A-Za-z0-9_@.+-]*', login)
            or '..' in login):
        raise ValueError('explicit runtime account required')
    return login


def program_uri(login, name):
    check_login(login); check_program_name(name)
    return 'file:///auto/cache/' + login + '/matvey/' + name + '?raw=False'


def check_program_uri(value, owner_login):
    check_login(owner_login)
    if not isinstance(value, str) or '%' in value or '\\' in value:
        raise ValueError('literal owned program URI required')
    parsed = urlsplit(value)
    if parsed.scheme != 'file' or parsed.netloc or parsed.fragment or parsed.query != 'raw=False':
        raise ValueError('explicit owned file URI required')
    pieces = parsed.path.split('/')
    if len(pieces) != 6 or pieces[:4] != ['', 'auto', 'cache', owner_login] or pieces[4] != 'matvey':
        raise ValueError('program outside runtime account matvey directory')
    check_program_name(pieces[5])
    if value != program_uri(owner_login, pieces[5]):
        raise ValueError('noncanonical owned program URI')
    return value
