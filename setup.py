from typing import List, Tuple, Union, Text
from setuptools import setup, find_packages


ClassifiersType = Union[List[Text], Tuple[Text]]
VersionType = Union[List[int], Tuple[int, int, int]]

VERSION: VersionType = 0, 1, 3
README_FN: Text = "README.md"

__python_requires__: Text = ">=3.7"
__content_type__: Text = "text/markdown"
__version__: Text = '.'.join(map(str, VERSION))
__name__ = "ProxyScanIOApi"

__author__: Text = "NIKDISSV"
__email__: Text = "nikdissv.contact@gmail.com"
__url__: Text = "https://github.com/NIKDISSV-Forever/proxyscan/"

__description__ = __long_description__ = "Получи список прокси, с множеством параметров, с помощью API."
try:
    with open(README_FN, encoding="UTF-8") as ReadMe:
        __long_description__ = ReadMe.read()
except:
    pass


__classifiers__: ClassifiersType = ["Programming Language :: Python :: 3",
                                    "Operating System :: OS Independent",
                                    # "License :: AGPL-3.0-only",
                                    ]

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=__long_description__,
    long_description_content_type=__content_type__,
    url=__url__,
    packages=find_packages(),
    classifiers=__classifiers__,
    python_requires=__python_requires__,
)
