import os
import uuid
import sys

from setuptools import setup
from pip.req import parse_requirements

with open("./pushbullet/__version__.py") as version_file:
    version = version_file.read().split("\"")[1]

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

install_reqs = parse_requirements("requirements.txt",  session=uuid.uuid1())



def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            return f.read()
    except IOError:
        return ""

setup(
    name = "pushbullet.py",
    version = version,
    author = "Richard Borcsik",
    author_email = "borcsikrichard@gmail.com",
    description = ("A simple python client for pushbullet.com"),
    license = "MIT",
    keywords = "push android pushbullet notification",
    url = "https://github.com/randomchars/pushbullet.py",
    download_url="https://github.com/randomchars/pushbullet.py/tarball/" + version,
    packages=['pushbullet'],
    long_description=read('readme.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    install_requires=[str(ir.req) for ir in install_reqs]
)
