# Copyright (c) 2021 Ben Maddison. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""rpkimancer documentation config."""

from __future__ import annotations

import datetime
import importlib.metadata

import rpkimancer_doa

import sphinx_readable_theme

_dist = importlib.metadata.distribution(rpkimancer_doa.__name__)
_buildtime = datetime.datetime.utcnow()

# -- Project Information

project = "RPKI Discard Origin Authorizations"
author = _dist.metadata["author"]

_from_year = 2021
_to_year = _buildtime.year
if _from_year < _to_year:
    _year_range = f"{_from_year}-{_to_year}"
else:
    _year_range = f"{_from_year}"
copyright = f"{_year_range}, {author}"

release = _dist.version
version = ".".join(release.split(".")[:2])

# -- General configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_xml2rfc",
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
exclude_patterns = []

# -- HTML output

html_theme = "readable"
html_theme_path = [sphinx_readable_theme.get_html_theme_path()]
html_static_path = ["_static"]
html_sidebars = {"**": []}

# -- Autodoc configuration

autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_description_target = "all"


# -- Intersphinx configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "rpkimancer": ("https://benmaddison.github.io/rpkimancer/main/", None),
}

# -- Markdown processing

myst_enable_extensions = [
    "colon_fence",
]

# -- xml2rfc document generation

xml2rfc_drafts = ["draft-spaghetti-sidrops-rpki-doa"]
xml2rfc_sources = ["RpkiDiscardOriginAuthorization-2021.asn"]
xml2rfc_autogen_tag_re = r"^\d\d$"
