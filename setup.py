from setuptools import setup, find_packages

__content_type__ = "text/markdown"
__url__ = "https://github.com/NIKDISSV-Forever/proxyscan"

with open ('VERSION', 'r') as fv:
	__version__ = fv.read()

with open("README.md", "r") as frm:
    __long_description__ = frm.read()

__description__ = "Получи список прокси, с множеством параметров, с помощью API."

setup (
    name = 'proxyscan-api',
    version = __version__,
    author = 'NIKDISSV',
    description = __description__,
    long_description = __long_description__,
    long_description_content_type = __content_type__,
    url = __url__,
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU AGPL :: v3",
        "Language :: English :: Russian"
    ],
)
