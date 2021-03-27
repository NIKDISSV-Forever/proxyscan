from setuptools import setup, find_packages

__content_type__ = "text/markdown"
__url__ = "https://github.com/NIKDISSV-Forever/proxyscan"
__classifiers__ = ["Programming Language :: Python :: 3", "Operating System :: OS Independent"]

VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))

with open("README.md", "r", encoding="UTF-8") as frm:
    __long_description__ = frm.read()

__description__ = "Получи список прокси, с множеством параметров, с помощью API."

setup (
    name = 'proxyscanIOApi',
    version = __version__,
    author = 'NIKDISSV',
    author_email = 'nikdissv.contact@gmail.com',
    description = __description__,
    long_description = __long_description__,
    long_description_content_type = __content_type__,
    url = __url__,
    packages = find_packages(),
    classifiers = __classifiers__,
    #"License :: AGPL-3.0-only"
    python_requires='>=3.6',
)
