import setuptools

with open('README.md', encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="EasyProxies",

    version="0.1.2",

    author="Nikita (NIKDISSV)",
    author_email="nikdissv.forever@protonmail.com",

    description="A simple and quick way to get a proxy.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/NIKDISSV-Forever/proxyscan",

    packages=setuptools.find_packages(),

    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    python_requires='>=3.6',
)
