import sys

PY2 = sys.version_info[0] == 2

if PY2:

    standard_b64encode = lambda x: x.encode("base64")

else:

    from base64 import standard_b64encode

__all__ = ['standard_b64encode']
