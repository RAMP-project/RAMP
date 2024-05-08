# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys


sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../.."))
sys.path.insert(0, os.path.abspath("../../.."))

from notebooks_convert import update_notebooks_rst_files

update_notebooks_rst_files()


def copy_readme():
    with open("../../README.rst", "r", encoding="utf8") as fp:
        data = fp.readlines()

    # Replace the reference to contributing guidelines with an internal link
    idx = data.index(
        "To contribute changes please consult our `Contribution guidelines <https://github.com/RAMP-project/RAMP/blob/main/CONTRIBUTING.md>`_\n"
    )
    data[idx] = (
        "To contribute changes please consult our `Contribution guidelines <contributing.html>`_\n"
    )
    with open("readme.rst", "w") as fp:
        fp.writelines(data)


def copy_contributing():
    with open("../../CONTRIBUTING.md", "r", encoding="utf8") as fp:
        data = fp.readlines()

    # Change the title of the file
    data[0] = "# Contribute\n"
    with open("contributing.md", "w") as fp:
        fp.writelines(data)


copy_readme()
copy_contributing()
# -- Project information -----------------------------------------------------

project = "RAMP"
copyright = "2022, Author List"
author = "Author List"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "nbsphinx",
    "IPython.sphinxext.ipython_console_highlighting",
    "sphinx.ext.mathjax",
    "sphinx.ext.coverage",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx_copybutton",
    "sphinx.ext.autosectionlabel",
    "sphinx_wagtail_theme",
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#


html_theme = "sphinx_wagtail_theme"
html_theme_options = dict(
    project_name="RAMP Documentation",
)
# html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# copy btn settings
copybutton_prompt_text = "<AxesSubplot:>"
