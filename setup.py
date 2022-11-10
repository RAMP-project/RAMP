
from setuptools import find_packages,setup
from ramp._version import __version__


setup(
    name = "ramp",
    description= "An open-source python package for building bottom-up stochastic model for generating multi-energy load profiles",
    long_description = open("README.rst").read(),
    author_email = "f.lombardi@tudelft.nl",
    url= "https://github.com/RAMP-project/RAMP",
    version = __version__,
    packages= find_packages(),
    license="European Union Public License 1.2",
    python_requires = ">.3.6.0",
    package_data={"": ["*.txt", "*.dat", "*.doc", "*.rst","*.xlsx"]},
    install_requires = [
        "pandas >= 1.3.3",
        "numpy >= 1.21.2",
        "xlsxwriter >= 1.3.7",
        "matplotlib >= 3.3.4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6"
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
)
