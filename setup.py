import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lisa",
    version="0.0.1",
    author="Lisa-Yao Gan",
    author_email="ga27bil@mytum.de",
    description="A fun little program that lets you transcribe and generate piano music",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.ldv.ei.tum.de/komcrea/musik/-/tree/master",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows 64 Bit",
    ],
    python_requires='=3.7',
)