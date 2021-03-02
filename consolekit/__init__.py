#!/usr/bin/env python3
#
#  __init__.py
"""
Additional utilities for `click <https://click.palletsprojects.com/en/7.x/>`_.

.. attention::

	``consolekit`` disables Python's readline history to prevent unrelated histories appearing for prompts.
	If the original behaviour is desired run:

	.. code-block:: python

		import readline
		readline.set_history_length(-1)
		readline.set_auto_history(True)

"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import sys
from functools import partial

# 3rd party
import click

# this package
from consolekit import commands, input, terminal_colours, tracebacks, utils  # pylint: disable=redefined-builtin
from consolekit.commands import SuggestionGroup
from consolekit.options import _Option

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "1.1.0"
__email__: str = "dominic@davis-foster.co.uk"

if not bool(getattr(sys, "ps1", sys.flags.interactive)):  # pragma: no cover
	try:
		# stdlib
		import readline
		readline.set_history_length(0)
		readline.set_auto_history(False)
	except (ImportError, AttributeError):
		# Attribute error on PyPy, ImportError on Windows etc.
		pass

__all__ = [
		"CONTEXT_SETTINGS",
		"click_command",
		"click_group",
		"option",
		"SuggestionGroup",
		]

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)

click_command = partial(click.command, context_settings=CONTEXT_SETTINGS)
"""
Shortcut to :func:`click.command`, with the ``-h``/``--help`` option enabled and a max width of ``120``.
"""

click_group = partial(click.group, context_settings=CONTEXT_SETTINGS, cls=SuggestionGroup)
"""
Shortcut to :func:`click.group`, with the ``-h``/``--help`` option enabled and a max width of ``120``.
"""

option = partial(click.option, cls=_Option)
"""
Shortcut to :func:`click.option`, but using :func:`consolekit.input.confirm` when prompting for a boolean flag.
"""

# Fixes intersphinx links
click.Command.__module__ = "click"
click.Argument.__module__ = "click"
click.Abort.__module__ = "click"
click.Option.__module__ = "click"
click.ParamType.__module__ = "click"
click.Parameter.__module__ = "click"
click.Context.__module__ = "click"
click.HelpFormatter.__module__ = "click"
click.Group.__module__ = "click"
click.OptionParser.__module__ = "click"
