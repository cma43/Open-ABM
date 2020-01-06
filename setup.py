import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="openabm",
    version="1.0.0",
    description="A Python framework for agent-based modeling based on MESA",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.ncsu.edu/cmartman/Open-ABM",
    author="Conor M. Artman",
    author_email="cmartman@ncsu.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["mesa"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)