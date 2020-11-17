#!/usr/bin/env python3
#
#  options.py
"""
Command line options.

.. versionadded:: 0.4.0
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
from typing import Any, Callable

# 3rd party
import click
from click import Context, Option

__all__ = ["verbose_option", "version_option", "colour_option", "force_option", "no_pager_option"]


def verbose_option(help_text: str = "Show verbose output.") -> Callable:
	"""
	Adds an option (via the parameter ``verbose``: :class:`int`) to enable verbose output.

	The option can be provided multiple times by the user.

	:param help_text: The help text for the option.

	:rtype:

	.. versionadded:: 0.4.0
	"""

	return click.option(
			"-v",
			"--verbose",
			count=True,
			help=help_text,
			)


def version_option(callback: Callable[[Context, Option, int], Any]) -> Callable:
	"""
	Adds an option to show the version and exit.

	The option can be provided multiple times by the user.

	:param callback: The callback to invoke when the option is provided.

	:rtype:

	.. versionadded:: 0.4.0
	"""

	return click.option(
			"--version",
			count=True,
			expose_value=False,
			is_eager=True,
			help="Show the version and exit.",
			callback=callback,  # type: ignore
			)


def colour_option(help_text="Whether to use coloured output.") -> Callable:
	"""
	Adds an option (via the parameter ``colour``: :class:`bool`) to enable verbose output.

	:param help_text: The help text for the option.

	:rtype:

	.. versionadded:: 0.4.0
	"""

	return click.option(
			"--colour/--no-colour",
			is_flag=True,
			default=None,
			help=help_text,
			)


def force_option(help_text: str) -> Callable:
	"""
	Decorator to add the ``-f / --force`` option to a click command.

	:param help_text: The help text for the option.

	:rtype:

	.. versionadded:: 0.5.0
	"""

	return click.option(
			"-f",
			"--force",
			is_flag=True,
			default=False,
			help=help_text,
			)


def no_pager_option(help_text="Disable the output pager.") -> Callable:
	"""
	Decorator to add the ``--no-pager`` option to a click command.

	:param help_text: The help text for the option.

	:rtype:

	.. versionadded:: 0.5.0
	"""

	return click.option(
			"--no-pager",
			is_flag=True,
			default=False,
			help=help_text,
			)
