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
#  MultiValueOption based on https://stackoverflow.com/a/48394004
#  Copyright (c) 2018 Stephen Rauch <https://stackoverflow.com/users/7311767/stephen-rauch>
#  CC BY-SA 3.0
#
#  MultiValueOption based on https://github.com/pallets/click
#  Copyright 2014 Pallets
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |      * Redistributions of source code must retain the above copyright notice,
#  |        this list of conditions and the following disclaimer.
#  |      * Redistributions in binary form must reproduce the above copyright notice,
#  |        this list of conditions and the following disclaimer in the documentation
#  |        and/or other materials provided with the distribution.
#  |      * Neither the name of the copyright holder nor the names of its contributors
#  |        may be used to endorse or promote products derived from this software without
#  |        specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  |  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  |  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  |  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#  |  OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  |  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  |  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  |  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  |  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  |  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from typing import Any, Callable, List, Optional, cast

# 3rd party
import click
from click import Context, Option, OptionParser

# this package
from consolekit._types import Callback, _ConvertibleType

__all__ = [
		"verbose_option",
		"version_option",
		"colour_option",
		"force_option",
		"no_pager_option",
		"MultiValueOption",
		]


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
			callback=cast(Callback, callback),
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


class MultiValueOption(click.Option):
	"""
	Subclass of :class:`click.Option` that behaves like argparse's ``nargs='+'``.

	:param param_decls: The parameter declarations for this option or argument.
		This is a list of flags or argument names.
	:param show_default: Controls if the default value should be shown on the help page.
		Normally, defaults are not shown.
		If this value is a string, it shows the string instead of the value.
		This is particularly useful for dynamic options.
	:param help: The help string.
	:param hidden: Hide this option from help outputs.
	:param type: The type that should be used.  Either a :class:`click.ParamType` or a Python type.
		The later is converted into the former automatically if supported.
	:param required: Controls whether this is optional.
	:param default: The default value if omitted.
		This can also be a callable, in which case it's invoked when the default is needed without any arguments.
	:param callback: A callback that should be executed after the parameter was matched.
		This is called as ``fn(ctx, param, value)`` and needs to return the value.
	:param metavar: How the value is represented in the help page.
	:param expose_value: If :py:obj:`True` then the value is passed onwards to the command callback
		and stored on the context, otherwise it's skipped.
	:param is_eager: Eager values are processed before non eager ones.

	.. versionadded:: 0.6.0
	"""

	def __init__(
			self,
			param_decls: Optional[List[str]] = None,
			show_default: bool = False,
			help: Optional[str] = None,
			hidden: bool = False,
			type: Optional[_ConvertibleType] = None,
			required: bool = False,
			default: Optional[Any] = None,
			callback: Optional[Callback] = None,
			metavar: Optional[str] = None,
			expose_value: bool = True,
			is_eager: bool = False,
			):

		super().__init__(
				show_default=show_default,
				help=help,
				hidden=hidden,
				param_decls=param_decls,
				type=type,
				required=required,
				default=default,
				callback=callback,
				metavar=metavar,
				expose_value=expose_value,
				is_eager=is_eager,
				)
		self._previous_parser_process: Optional[Callable] = None
		self._eat_all_parser: Optional[click.parser.Option] = None

	def add_to_parser(self, parser: OptionParser, ctx: Context):
		"""

		:param parser:
		:param ctx:
		"""

		def parser_process(value, state):
			# method to hook to the parser.process
			done = False
			value = [value]
			# grab everything up to the next option
			while state.rargs and not done:
				for prefix in self._eat_all_parser.prefixes:  # type: ignore
					if state.rargs[0].startswith(prefix):
						done = True
				if not done:
					value.append(state.rargs.pop(0))

			value = tuple(value)

			# call the actual process
			self._previous_parser_process(value, state)  # type: ignore

		retval = super().add_to_parser(parser, ctx)

		for name in self.opts:
			our_parser: Optional[click.parser.Option] = parser._long_opt.get(name) or parser._short_opt.get(name)
			if our_parser:
				self._eat_all_parser = our_parser
				self._previous_parser_process = our_parser.process
				our_parser.process = parser_process  # type: ignore
				break

		return retval
