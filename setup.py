from setuptools import find_packages, setup

exec(open("ramp/_version.py").read())


setup(
    name="rampdemand",
    description="An open-source python package for building bottom-up stochastic model for generating multi-energy load profiles",
    long_description=open("README.rst", encoding="utf8").read(),
    long_description_content_type="text/x-rst",
    author_email="f.lombardi@tudelft.nl",
    url="https://github.com/RAMP-project/RAMP",
    version=__version__,
    packages=find_packages(),
    license="European Union Public License 1.2",
    python_requires="<=3.11",
    package_data={"": ["*.txt", "*.dat", "*.doc", "*.rst", "*.xlsx", "*.csv"]},
    install_requires=[
        "pandas >= 1.3.3",
        "numpy >= 1.21.2",
        "xlsxwriter >= 1.3.7",
        "matplotlib >= 3.3.4",
        "openpyxl >= 3.0.6",
        "tqdm",
        "plotly",
        "multiprocess",
    ],
    # classifiers=[
    #     "Programming Language :: Python :: 3.7",
    #     "Programming Language :: Python :: 3.8",
    #     "Programming Language :: Python :: 3.9",
    #     "Intended Audience :: End Users/Desktop",
    #     "Intended Audience :: Developers",
    #     "Intended Audience :: Science/Research",
    #     "Operating System :: MacOS :: MacOS X",
    #     "Operating System :: Microsoft :: Windows",
    #     "Programming Language :: Python",
    #     "Topic :: Scientific/Engineering",
    # ],
    entry_points={
        "console_scripts": [
            "ramp=ramp.cli:main",
            "ramp_convert=ramp.ramp_convert_old_input_files:cli",
        ],
    },
)
