import os
import sys

from setuptools import setup

import pushbullet

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pushbullet.py",
    version = pushbullet.__version__,
    author = "Richard Borcsik",
    author_email = "richard@borcsik.com",
    description = ("A simple python client for pushbullet.com"),
    license = "MIT",
    keywords = "push android pushbullet notification",
    url = "https://github.com/randomchars/pushbullet.py",
    download_url="https://github.com/randomchars/pushbullet.py/tarball/" + pushbullet.__version__,
    packages=['pushbullet'],
     package_data={'': ['LICENSE', 'readme.md', 'changelog.md'],},
    long_description=read('readme.md') + "\n\n" + read("changelog.md"),
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
    install_requires=[
          'requests>=1.0.0',
      ]
)