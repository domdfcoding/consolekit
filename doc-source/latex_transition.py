# 3rd party
from docutils import nodes
from docutils.transforms.misc import Transitions
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.nodes import process_only_nodes
from sphinx.writers.latex import LaTeXTranslator


class TransitionTransform(Transitions):
	default_priority = Transitions.default_priority - 10

	def visit_transition(self, node):
		index = node.parent.index(node)
		error = None
		if (
				index == 0 or isinstance(node.parent[0], nodes.title) and
				(index == 1 or isinstance(node.parent[1], nodes.subtitle) and index == 2)
				):
			if isinstance(node.parent, (nodes.document, nodes.section)):
				error = self.document.reporter.error(
						"Document or section may not begin with a transition.",
						source=node.source,
						line=node.line,
						)
		elif isinstance(node.parent[index - 1], nodes.transition):
			error = self.document.reporter.error(
					'At least one body element must separate transitions; '
					'adjacent transitions are not allowed.',
					source=node.source,
					line=node.line
					)

		if error:
			# Insert before node and update index.
			node.parent.insert(index, error)
			index += 1

		assert index < len(node.parent)  # skipcq

		if index != len(node.parent) - 1:
			# No need to move the node.
			return

		# Node behind which the transition is to be moved.
		sibling = node

		# While sibling is the last node of its parent.
		while index == len(sibling.parent) - 1:
			sibling = sibling.parent
			# If sibling is the whole document (i.e. it has no parent).
			if sibling.parent is None:
				# Transition at the end of document.  Do not move the
				# transition up, and place an error behind.
				error = self.document.reporter.error("Document may not end with a transition.", line=node.line)
				node.parent.insert(node.parent.index(node) + 1, error)
				return

			index = sibling.parent.index(sibling)

		# Remove the original transition node.
		node.parent.remove(node)
		# Insert the transition after the sibling.
		sibling.parent.insert(index + 1, node)


class TransitionTransform(Transitions):
	default_priority = Transitions.default_priority - 10

	def visit_transition(self, node):

		if isinstance(node.parent, addnodes.only):
			process_only_nodes(
					node.parent.parent,
					tags=self.document.settings.env.app.builder.tags,
					)


class TransitionDirective(SphinxDirective):

	def run(self):
		return [nodes.transition()]


def depart_desc_annotation(translator: LaTeXTranslator, node: addnodes.desc_annotation) -> None:
	translator.body.append("}}")
	parent = node.parent
	grandparent = parent.parent
	if len(grandparent) > 1:
		aunt = grandparent[grandparent.index(parent) + 1]

		if isinstance(parent, addnodes.desc_signature) and isinstance(aunt, addnodes.desc_signature):
			translator.body.append(r"\vspace{5px}")


class InlineRole(SphinxRole):

	def run(self):
		return [nodes.literal('', f"`{self.text}`")], []


def setup(app: Sphinx):
	app.add_directive("transition", TransitionDirective)
	app.add_transform(TransitionTransform)
	app.add_node(
			addnodes.desc_annotation,
			latex=(LaTeXTranslator.visit_desc_annotation, depart_desc_annotation),
			override=True
			)
	app.add_role("inline-code", InlineRole())
