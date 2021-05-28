# 3rd party
from domdf_python_tools.stringlist import StringList
from sphinx import addnodes
from sphinx.application import Sphinx  # nodep
from sphinx.config import Config  # nodep
from sphinx.writers.latex import LaTeXTranslator
from sphinxcontrib import toctree_plus


def visit_desc(translator: LaTeXTranslator, node: addnodes.desc) -> None:
	"""
	Visit an :class:`addnodes.desc` node and add a custom table of contents label for the item, if required.

	.. versionadded:: 0.3.0

	:param translator:
	:param node:
	"""

	translator.body.append(r"\needspace{5\baselineskip}")
	toctree_plus.visit_desc(translator, node)


def configure(app: Sphinx, config: Config):
	"""
	Configure Sphinx Extension.

	:param app: The Sphinx application.
	:param config:
	"""

	latex_elements = getattr(config, "latex_elements", {})

	latex_extrapackages = StringList(latex_elements.get("extrapackages", ''))
	latex_extrapackages.append(r"\usepackage{needspace}")
	latex_elements["extrapackages"] = str(latex_extrapackages)

	config.latex_elements = latex_elements  # type: ignore


def setup(app: Sphinx):
	"""
	Setup Sphinx Extension.

	:param app: The Sphinx application.
	"""

	app.connect("config-inited", configure)
	app.add_node(addnodes.desc, latex=(visit_desc, toctree_plus.depart_desc), override=True)

	return {"parallel_read_safe": True}
