from setuptools import setup, find_packages

__content_type__ = "text/markdown"
__url__ = "https://github.com/NIKDISSV-Forever/proxyscan"

VERSION = (0, 0, 3)
__version__ = '.'.join(map(str, VERSION[0:3]))

with open("README.md", "r") as frm:
    __long_description__ = frm.read()

__description__ = "Получи список прокси, с множеством параметров, с помощью API."

setup (
    name = 'proxyscan-api-NIKDISSV',
    version = __version__,
    author = 'NIKDISSV',
    author_email = 'nikdissv.contact@gmail.com',
    description = __description__,
    long_description = __long_description__,
    long_description_content_type = __content_type__,
    url = __url__,
    packages = find_packages(),
    classifiers = ["Programming Language :: Python :: 3", "License :: AGPL-3.0-only", "Operating System :: OS Independent"],
    python_requires='>=3.2',
)
