=============================
:mod:`consolekit.commands`
=============================

.. autosummary-widths:: 49/100

.. automodule:: consolekit.commands
	:no-members:
	:autosummary-members:

.. currentmodule:: consolekit.commands

.. latex:vspace:: -10px
.. autoclass:: ContextInheritingGroup

.. class:: MarkdownHelpCommand
		   MarkdownHelpGroup

	Bases: :class:`~.MarkdownHelpMixin`

	Subclasses of :class:`click.Command` and :class:`click.Group`
	which treat the help text as markdown and print a rendered representation.

	Tested in Gnome Terminal and Terminator (both libVTE-based), and PyCharm.
	libVTE has the best support.
	PyCharm's support for italics and strikethrough is poor.
	Support on Windows is, as expected, poor.

	Not tested on other terminals, but contributions are welcome to improve support.

	.. versionadded:: 0.8.0

	.. automethod:: MarkdownHelpCommand.parse_args

.. autoclass:: consolekit.commands.MarkdownHelpMixin
	:no-autosummary:

.. class:: RawHelpCommand
		   RawHelpGroup

	Bases: :class:`~.RawHelpMixin`

	Subclasses of :class:`click.Command` and :class:`click.Group`
	which leave the help text unformatted.

	.. versionadded:: 0.8.0

.. autoclass:: consolekit.commands.RawHelpMixin
	:no-autosummary:

.. autoclass:: consolekit.commands.SuggestionGroup
	:no-autosummary:
