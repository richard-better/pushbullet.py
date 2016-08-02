def _magic_get_file_type(f, _):
    file_type = magic.from_buffer(f.read(1024), mime=True)
    f.seek(0)
    return maybe_decode(file_type)


def _guess_file_type(_, filename):
    return mimetypes.guess_type(filename)[0]


# return str on python3.  Don't want to unconditionally
# decode because that results in unicode on python2
def maybe_decode(s):
    if str == bytes:
        return s.decode('utf-8')
    else:
        return s


try:
    import magic
except ImportError:
    import mimetypes
    get_file_type = _guess_file_type
else:
    get_file_type = _magic_get_file_type
