
try:
    from magic import from_buffer as magic_from_buffer
except ImportError:
    import mimetypes


def get_file_type(file, filename):
    try:
        file_type = magic_from_buffer(file.read(1024), mime=True)
        file.seek(0)
        return maybe_decode(file_type)
    except NameError:
        return mimetypes.guess_type(filename)[0]


# return str on python3.  Don't want to unconditionally
# decode because that results in unicode on python2
def maybe_decode(s):
    try:
        decoded = s.decode('utf-8')
    except AttributeError as e:
        decoded = s
    return decoded

