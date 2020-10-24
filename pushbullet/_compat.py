import sys


def _py2_b64encode(x):
    return x.encode("base64")


if sys.version_info[0] == 2:
    standard_b64encode = _py2_b64encode
else:
    from base64 import standard_b64encode

__all__ = ["standard_b64encode"]
