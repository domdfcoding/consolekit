#!/usr/bin/env python3
#
#  commands.py
"""
Customised click commands and command groups.

.. versionadded:: 0.8.0
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  MarkdownHelpCommand.parse_args based on https://github.com/pallets/click
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
import difflib
from textwrap import indent
from typing import List, Optional, Tuple

# 3rd party
import click
from click.core import iter_params_for_processing
from click.parser import split_opt
from click.utils import make_str
from domdf_python_tools.stringlist import DelimitedList
from domdf_python_tools.words import Plural
from mistletoe import block_token  # type: ignore

# this package
from consolekit.terminal_colours import ColourTrilean, resolve_color_default, strip_ansi
from consolekit.utils import TerminalRenderer

__all__ = [
		"MarkdownHelpCommand",
		"MarkdownHelpGroup",
		"MarkdownHelpMixin",
		"RawHelpCommand",
		"RawHelpGroup",
		"RawHelpMixin",
		"SuggestionGroup",
		]

_argument = Plural("argument", "arguments")


class RawHelpMixin:
	"""
	Mixin class for :class:`click.Command` and :class:`click.Group` which leaves the help text unformatted.

	.. seealso::

		* :class:`~.RawHelpCommand`
		* :class:`~.RawHelpGroup`

	.. tip:: This can be combined with groups such as :class:`~.SuggestionGroup`.

	.. versionadded:: 0.8.0
	"""

	help: Optional[str]  # noqa: A003  # pylint: disable=redefined-builtin

	def format_help_text(self, ctx: click.Context, formatter: click.formatting.HelpFormatter):
		"""
		Writes the help text to the formatter if it exists.

		:param ctx:
		:param formatter:
		"""

		formatter.write('\n')
		formatter.write(indent((self.help or ''), "  "))
		formatter.write('\n')


class RawHelpCommand(RawHelpMixin, click.Command):  # lgtm [py/conflicting-attributes]
	"""
	Subclass of :class:`click.Command` which leaves the help text unformatted.

	.. versionadded:: 0.8.0
	"""


class RawHelpGroup(RawHelpMixin, click.Group):  # lgtm [py/conflicting-attributes]
	"""
	Subclass of :class:`click.Group` which leaves the help text unformatted.

	.. versionadded:: 0.8.0
	"""


class MarkdownHelpMixin:
	"""
	Mixin class for :class:`click.Command` and :class:`click.Group` which treats the help text as markdown
	and prints a rendered representation.

	.. seealso::

		* :class:`~.MarkdownHelpCommand`
		* :class:`~.MarkdownHelpGroup`

	.. tip:: This can be combined with groups such as :class:`~.SuggestionGroup`.

	Tested in Gnome Terminal and Terminator (both libVTE-based), and PyCharm.
	libVTE has the best support.
	PyCharm's support for italics and strikethrough is poor.
	Support on Windows is, as expected, poor.

	Not tested on other terminals, but contributions are welcome to improve support.

	.. versionadded:: 0.8.0
	"""  # noqa: D400

	help: Optional[str]  # noqa: A003  # pylint: disable=redefined-builtin
	no_args_is_help: bool
	_colour: ColourTrilean = None

	def format_help_text(self, ctx: click.Context, formatter: click.formatting.HelpFormatter):
		"""
		Writes the help text to the formatter if it exists.

		:param ctx:
		:param formatter:
		"""

		doc = block_token.Document(self.help or '')

		with TerminalRenderer() as renderer:
			rendered_doc = indent(renderer.render(doc).strip(), "  ")

		if resolve_color_default(self._colour) is False:
			# Also remove 'COMBINING LONG STROKE OVERLAY', used for strikethrough.
			rendered_doc = strip_ansi(rendered_doc).replace('̶', '')

		formatter.write('\n')
		formatter.write(rendered_doc)
		formatter.write('\n')


class MarkdownHelpCommand(MarkdownHelpMixin, click.Command):  # lgtm [py/conflicting-attributes]
	"""
	Subclass of :class:`click.Command` which treats the help text as markdown
	and prints a rendered representation.

	Tested in Gnome Terminal and Terminator (both libVTE-based), and PyCharm.
	libVTE has the best support.
	PyCharm's support for italics and strikethrough is poor.
	Support on Windows is, as expected, poor.

	Not tested on other terminals, but contributions are welcome to improve support.

	.. versionadded:: 0.8.0
	"""  # noqa: D400

	def parse_args(self, ctx: click.Context, args: List[str]) -> List[str]:
		"""
		Parse the given arguments and modify the context as necessary.

		:param ctx:
		:param args:
		"""

		# This is necessary to parse any --colour/--no-colour commands before generating the help,
		# to ensure the option is honoured.

		if not args and self.no_args_is_help and not ctx.resilient_parsing:
			click.echo(ctx.get_help(), color=ctx.color)
			ctx.exit()

		parser = self.make_parser(ctx)
		opts, args, param_order = parser.parse_args(args=args)

		self._colour = opts.get("colour", ctx.color)

		for param in iter_params_for_processing(param_order, self.get_params(ctx)):
			value, args = param.handle_parse_result(ctx, opts, args)

		if args and not ctx.allow_extra_args and not ctx.resilient_parsing:
			args_string = DelimitedList(map(make_str, args))
			ctx.fail(f"Got unexpected extra {_argument(len(args))} ({args_string: })")

		ctx.args = args
		return args


class MarkdownHelpGroup(MarkdownHelpMixin, click.Group):  # lgtm [py/conflicting-attributes]
	"""
	Subclass of :class:`click.Group` which treats the help text as markdown
	and prints a rendered representation.

	Tested in Gnome Terminal and Terminator (both libVTE-based), and PyCharm.
	libVTE has the best support.
	PyCharm's support for italics and strikethrough is poor.
	Support on Windows is, as expected, poor.

	Not tested on other terminals, but contributions are welcome to improve support.

	.. versionadded:: 0.8.0
	"""  # noqa: D400

	def parse_args(self, ctx: click.Context, args: List[str]) -> List[str]:
		"""
		Parse the given arguments and modify the context as necessary.

		:param ctx:
		:param args:
		"""

		# This is necessary to parse any --colour/--no-colour commands before generating the help,
		# to ensure the option is honoured.

		if not args and self.no_args_is_help and not ctx.resilient_parsing:
			click.echo(ctx.get_help(), color=ctx.color)
			ctx.exit()

		rest = MarkdownHelpCommand.parse_args(self, ctx, args)  # type: ignore
		if self.chain:
			ctx.protected_args = rest
			ctx.args = []
		elif rest:
			ctx.protected_args, ctx.args = rest[:1], rest[1:]

		return ctx.args


class SuggestionGroup(click.Group):
	"""
	Subclass of :class:`click.Group` which suggests the most similar command if the command is not found.

	.. versionadded 0.2.0

	.. versionchanged:: 0.8.0

		Moved to :mod:`consolekit.commands`.
	"""

	def resolve_command(
			self,
			ctx: click.Context,
			args: List[str],
			) -> Tuple[str, click.Command, List[str]]:  # noqa: D102
		"""
		Resolve the requested command belonging to this group, and print a suggestion if it can't be found.

		:param ctx:
		:param args:

		:return: The name of the matching command,
			the :class:`click.Command` object itself,
			and any remaining arguments.
		"""

		cmd_name = make_str(args[0])
		original_cmd_name = cmd_name

		# Get the command
		cmd = self.get_command(ctx, cmd_name)

		# If we can't find the command but there is a normalization
		# function available, we try with that one.
		if cmd is None and ctx.token_normalize_func is not None:
			cmd_name = ctx.token_normalize_func(cmd_name)
			cmd = self.get_command(ctx, cmd_name)

		# If we don't find the command we want to show an error message
		# to the user that it was not provided.
		# However, there is something else we should do:
		# if the first argument looks like an option we want to kick off parsing again
		# for arguments to resolve things like --help which now should go to the main place.
		if cmd is None and not ctx.resilient_parsing:
			if split_opt(cmd_name)[0]:
				self.parse_args(ctx, ctx.args)

			closest = difflib.get_close_matches(original_cmd_name, self.commands, n=1)
			message = [f"No such command '{original_cmd_name}'."]
			if closest:
				message.append(f"The most similar command is {closest[0]!r}.")
			ctx.fail('\n'.join(message))

		# TODO: cmd here is Optional[click.Command], typeshed says it should be just click.Command
		#  I think typeshed is wrong.
		#  https://github.com/python/typeshed/blob/484c014665cdf071b292dd9630f207c03e111895/third_party/2and3/click/core.pyi#L171
		return cmd_name, cmd, args[1:]  # type: ignore
