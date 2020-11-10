#!/usr/bin/env python3
#
#  __init__.py
"""
Additional utilities for `click <https://click.palletsprojects.com/en/7.x/>`_.
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
import difflib
import sys
from functools import partial

# 3rd party
import click
from click.parser import split_opt
from click.utils import make_str

# this package
from consolekit.input import confirm, prompt

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.3.0"
__email__: str = "dominic@davis-foster.co.uk"

if not bool(getattr(sys, "ps1", sys.flags.interactive)):

	try:
		# stdlib
		import readline
		readline.set_history_length(0)
		# Ref: https://github.com/python/typeshed/pull/4688
		readline.set_auto_history(False)  # type: ignore  # TODO
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


class SuggestionGroup(click.Group):
	"""
	Subclass of :class:`click.Group` which suggests the most similar command if the command is not found.

	.. versionadded 0.3.0
	"""

	def resolve_command(self, ctx, args):  # noqa: D102
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
		# to the user that it was not provided.  However, there is
		# something else we should do: if the first argument looks like
		# an option we want to kick off parsing again for arguments to
		# resolve things like --help which now should go to the main
		# place.
		if cmd is None and not ctx.resilient_parsing:
			if split_opt(cmd_name)[0]:
				self.parse_args(ctx, ctx.args)

			closest = difflib.get_close_matches(original_cmd_name, self.commands, n=1)[0]
			message = [f"No such command '{original_cmd_name}'."]
			if closest:
				message.append(f"The most similar command is {closest!r}.")
			ctx.fail("\n".join(message))

		return cmd_name, cmd, args[1:]


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)
click_command = partial(click.command, context_settings=CONTEXT_SETTINGS)
click_group = partial(click.group, context_settings=CONTEXT_SETTINGS, cls=SuggestionGroup)


class _Option(click.Option):

	def prompt_for_value(self, ctx):
		"""
		This is an alternative flow that can be activated in the full
		value processing if a value does not exist. It will prompt the
		user until a valid value exists and then returns the processed
		value as result.
		"""  # noqa: D400

		# Calculate the default before prompting anything to be stable.
		default = self.get_default(ctx)

		# If this is a prompt for a flag we need to handle this
		# differently.
		if self.is_bool_flag:
			return confirm(self.prompt, default)

		return prompt(
				self.prompt,
				default=default,
				type=self.type,
				hide_input=self.hide_input,
				show_choices=self.show_choices,
				confirmation_prompt=self.confirmation_prompt,
				value_proc=lambda x: self.process_value(ctx, x),
				)


option = partial(click.option, cls=_Option)
