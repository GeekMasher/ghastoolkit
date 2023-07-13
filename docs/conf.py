import os
import sys
from sphinx.application import Sphinx

sys.path.append(os.path.join(os.getcwd(), ".."))


# -- Project information -----------------------------------------------------

from ghastoolkit import (
    __title__ as project,
    __copyright__ as copyright,
    __version__ as release,
    __author__ as author,
)

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
]

master_doc = "index"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
html_theme = "alabaster"
html_static_path = ["static"]

html_logo = "static/AdvancedSecurity.png"

htmlhelp_basename = f"{project}Doc"

# -- Options for Napoleon output ------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for manual page output ------------------------------------------
man_pages = [
    (master_doc, project, f"{project} Documentation", [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (
        master_doc,
        project,
        f"{project} Documentation",
        author,
        project,
        "One line description of project.",
        "Miscellaneous",
    ),
]


def setup(app: Sphinx):
    def cut_module_meta(app, what, name, obj, options, lines):
        """Remove metadata from autodoc output."""
        if what != "module":
            return

        lines[:] = [
            line for line in lines if not line.startswith((":copyright:", ":license:"))
        ]

    app.connect("autodoc-process-docstring", cut_module_meta)

