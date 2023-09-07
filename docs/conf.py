# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import django 

sys.path.insert(0, os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE']='cms_is2.settings'
django.setup()

source_suffix = ".rst"

master_doc = "index"

project = 'cms-is2-eq01'
copyright = '2023, Equipo 01'
author = 'Equipo 01'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'sphinx.ext.inheritance_diagram',

]

templates_path = ['_templates']
lenguage = 'es'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = []


latex_documents = [
    (
        "index",
        "cms-web",
        "cms-is2-eq01Documentation",
        "Equipo 01",
        "manual",
    )
]


man_pages = [
    (
        "index",
        "cms-web",
        "cms-is2-eq01 Documentation",
        ["Equipo 01"],
        1,
    )
]


texinfo_documents = [
    (
        "index",
        "cms-web",
        "cms-is2-eq01 Documentation",
        "Equipo 01",
        "cms-web",
        "one line description of proyect",
        "Miscellaneous",
    )
]