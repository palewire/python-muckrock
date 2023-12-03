"""Configure Sphinx configuration."""
import os
import sys
from datetime import datetime

# Insert the parent directory into the path
sys.path.insert(0, os.path.abspath(".."))

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "python-muckrock"
year = datetime.now().year
copyright = f"{year} palewire"

exclude_patterns = ["_build"]

html_theme = "palewire"
html_theme_options = {
    "canonical_url": f"https://palewi.re/docs/{project}/",
    "nosidebar": True,
}
