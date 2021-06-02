#!/usr/bin/env python3
#
#  options.py
"""
Command line options.

.. versionadded:: 0.4.0
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
#  MultiValueOption based on https://stackoverflow.com/a/48394004
#  Copyright (c) 2018 Stephen Rauch <https://stackoverflow.com/users/7311767/stephen-rauch>
#  CC BY-SA 3.0
#
#  MultiValueOption and auto_default_option based on https://github.com/pallets/click
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
import inspect
from typing import Any, Callable, Iterable, List, Optional, Tuple, TypeVar, cast

# 3rd party
import click
from click.decorators import _param_memo

# this package
import consolekit.input
from consolekit._types import Callback, _ConvertibleType

__all__ = [
		"verbose_option",
		"version_option",
		"colour_option",
		"force_option",
		"no_pager_option",
		"MultiValueOption",
		"flag_option",
		"auto_default_option",
		"auto_default_argument",
		"DescribedArgument",
		"_A",
		"_C",
		]

_A = TypeVar("_A", bound=click.Argument)
_C = TypeVar("_C", bound=click.Command)


class VerboseVersionCountType(click.IntRange):
	"""
	Subclass of :class:`click.IntRange` which doesn't show the range of valid values.

	.. versionadded:: 0.8.1
	"""

	def __init__(self):
		super().__init__(min=0)

	@staticmethod
	def _describe_range():  # pragma: no cover
		"""
		Describe the range for use in help text.
		"""

		return ''


def verbose_option(help_text: str = "Show verbose output.") -> Callable[[_C], _C]:
	"""
	Adds an option (via the parameter ``verbose``: :class:`int`) to enable verbose output.

	The option can be provided multiple times by the user.

	.. versionadded:: 0.4.0

	:param help_text: The help text for the option.
	"""

	return click.option(  # type: ignore
		"-v",
		"--verbose",
		count=True,
		help=help_text,
		type=VerboseVersionCountType(),
		)


def version_option(callback: Callable[[click.Context, click.Option, int], Any]) -> Callable[[_C], _C]:
	"""
	Adds an option to show the version and exit.

	The option can be provided multiple times by the user.
	The count is stored as an integer and passed as the third parameter to the callback function.

	.. versionadded:: 0.4.0

	:param callback: The callback to invoke when the option is provided.

	The callback function might look like:

	.. code-block:: python

		def version_callback(ctx: click.Context, param: click.Option, value: int):
			if not value or ctx.resilient_parsing:
				return

			if value > 1:
				click.echo(f"consolekit version {__version__}, Python {sys.version}")
			else:
				click.echo(f"consolekit version {__version__}")

			ctx.exit()

	"""

	return click.option(  # type: ignore
		"--version",
		count=True,
		expose_value=False,
		is_eager=True,
		help="Show the version and exit.",
		type=VerboseVersionCountType(),
		callback=cast(Callback, callback),
		)


def colour_option(help_text="Whether to use coloured output.") -> Callable[[_C], _C]:
	"""
	Adds an option (via the parameter ``colour``: :class:`bool`) to enable verbose output.

	.. versionadded:: 0.4.0

	:param help_text: The help text for the option.
	"""

	return flag_option(
			"--colour/--no-colour",
			default=None,
			help=help_text,
			)


def force_option(help_text: str) -> Callable[[_C], _C]:
	"""
	Decorator to add the ``-f / --force`` option to a click command.

	The value is exposed via the parameter ``force``: :class:`bool`.

	.. versionadded:: 0.5.0

	:param help_text: The help text for the option.
	"""

	return flag_option("-f", "--force", help=help_text)


def no_pager_option(help_text="Disable the output pager.") -> Callable[[_C], _C]:
	"""
	Decorator to add the ``--no-pager`` option to a click command.

	The value is exposed via the parameter ``no_pager``: :class:`bool`.

	.. versionadded:: 0.5.0

	:param help_text: The help text for the option.
	"""

	return flag_option("--no-pager", help=help_text)


def flag_option(*args, default: Optional[bool] = False, **kwargs) -> Callable[[_C], _C]:
	r"""
	Decorator to a flag option to a click command.

	.. versionadded:: 0.7.0

	:param \*args: Positional arguments passed to :func:`click.option`.
	:param default: The default state of the flag.
	:param \*\*kwargs: Keyword arguments passed to :func:`click.option`.
	"""

	return click.option(  # type: ignore
			*args,
			is_flag=True,
			default=default,
			**kwargs,
			)


def auto_default_option(*param_decls, **attrs) -> Callable[[_C], _C]:
	"""
	Attaches an option to the command, with a default value determined from the decorated function's signature.

	All positional arguments are passed as parameter declarations to :class:`click.Option`;
	all keyword arguments are forwarded unchanged (except ``cls``).
	This is equivalent to creating an :class:`click.Option` instance manually
	and attaching it to the :attr:`click.Command.params` list.

	.. versionadded:: 0.7.0

	:param cls: the option class to instantiate. This defaults to :class:`click.Option`.
	"""

	def decorator(f: _C) -> _C:
		option_attrs = attrs.copy()

		if "help" in option_attrs:
			option_attrs["help"] = inspect.cleandoc(option_attrs["help"])

		OptionClass = option_attrs.pop("cls", click.Option)

		option = OptionClass(param_decls, **option_attrs)
		_param_memo(f, option)

		_get_default_from_callback_and_set(f, option)

		return f

	return decorator


def _get_default_from_callback_and_set(command: click.Command, param: click.Parameter):
	if command.callback is not None:
		# The callback *can* be None, for a no-op

		if param.name is None:  # pragma: no cover
			raise ValueError("The parameter name cannot be None")

		signature: inspect.Signature = inspect.signature(command.callback)

		param_default = signature.parameters[param.name].default

		if param_default is not inspect.Signature.empty:
			param.default = param_default
			param.required = False


def auto_default_argument(*param_decls, **attrs) -> Callable[[_C], _C]:
	"""
	Attaches an argument to the command, with a default value determined from the decorated function's signature.

	All positional arguments are passed as parameter declarations to :class:`click.Argument`;
	all keyword arguments are forwarded unchanged (except ``cls``).
	This is equivalent to creating an :class:`click.Argument` instance manually
	and attaching it to the :attr:`click.Command.params` list.

	.. versionadded:: 0.8.0

	:param cls: the option class to instantiate. This defaults to :class:`click.Argument`.
	"""

	def decorator(f: _C) -> _C:
		ArgumentClass = attrs.pop("cls", click.Argument)
		argument = ArgumentClass(param_decls, **attrs)
		_param_memo(f, argument)

		_get_default_from_callback_and_set(f, argument)

		return f

	return decorator


class MultiValueOption(click.Option):
	"""
	Subclass of :class:`click.Option` that behaves like argparse's ``nargs='+'``.

	.. versionadded:: 0.6.0

	:param param_decls: The parameter declarations for this option or argument.
		This is a list of flags or argument names.
	:param show_default: Controls whether the default value should be shown on the help page.
		Normally, defaults are not shown.
		If this value is a string, it shows the string instead of the value.
		This is particularly useful for dynamic options.
	:param help: The help string.
	:param hidden: Hide this option from help outputs.
	:param type: The type that should be used.  Either a :class:`click.ParamType` or a Python type.
		The later is converted into the former automatically if supported.
	:param required: Controls whether this is optional.
	:param default: The default value if omitted.
		This can also be a callable, in which case it is invoked when the default is needed without any arguments.
	:param callback: A callback that should be executed after the parameter was matched.
		This is called as ``fn(ctx, param, value)`` and needs to return the value.
	:param metavar: How the value is represented in the help page.
	:param expose_value: If :py:obj:`True` then the value is passed onwards to the command callback
		and stored on the context, otherwise it is skipped.
	:param is_eager: Eager values are processed before non eager ones.

	Example usage:

	.. code-block:: python

		@click.option(
				"--select",
				type=click.STRING,
				help="The checks to enable",
				cls=MultiValueOption,
				)
		@click_command()
		def main(select: Iterable[str]):
			select = list(select)

	"""

	def __init__(
			self,
			param_decls: Optional[List[str]] = None,
			show_default: bool = False,
			help: Optional[str] = None,  # noqa: A002  # pylint: disable=redefined-builtin
			hidden: bool = False,
			type: Optional[_ConvertibleType] = None,  # noqa: A002  # pylint: disable=redefined-builtin
			required: bool = False,
			default: Optional[Any] = (),
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

	def add_to_parser(self, parser: click.OptionParser, ctx: click.Context):
		"""
		Add the :class:`~.MultiValueOption` to the given parser.

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

	def process_value(self, ctx: click.Context, value: Any) -> Optional[Tuple]:
		"""
		Given a value and context, converts the value as necessary.

		:param ctx:
		:param value:
		"""

		# If the value we were given is None we do nothing.
		# This way code that calls this can easily figure out if something was not provided.
		# Otherwise, it would be converted into an empty tuple for multiple invocations,
		# which is inconvenient.

		# assert isinstance(value, tuple), type(value)

		if value is not None:
			if isinstance(value, Iterable) and not isinstance(value, str):
				return tuple(self.type_cast_value(ctx, v) for v in value)
			elif value in ("()", str(self.default)) or not value:
				return self.default  # type: ignore
			else:
				return self.type_cast_value(ctx, value)
		else:
			return None


class _Option(click.Option):

	def prompt_for_value(self, ctx):
		"""
		This is an alternative flow that can be activated in the full value processing if a value does not exist.

		It will prompt the user until a valid value exists and then returns the processed value as result.
		"""

		# Calculate the default before prompting anything to be stable.
		default = self.get_default(ctx)

		prompt_string = cast(str, self.prompt)

		# If this is a prompt for a flag we need to handle this differently.
		if self.is_bool_flag:
			return consolekit.input.confirm(
					prompt_string,
					default,  # type: ignore
					)

		return consolekit.input.prompt(
				prompt_string,
				default=default,
				type=self.type,
				hide_input=self.hide_input,
				show_choices=self.show_choices,
				confirmation_prompt=self.confirmation_prompt,
				value_proc=lambda x: self.process_value(ctx, x),
				)


class DescribedArgument(click.Argument):
	r"""
	:class:`click.Argument` with an additional keyword argument and attribute giving a short description.

	This is not shown in the help text,
	but may be useful for manpages or HTML documentation where additional information can be provided.

	.. versionadded:: 1.2.0

	:param description:

	See :class:`click.Argument` and :class:`click.Parameter` for descriptions of the other keyword argu
	ments.

	.. attribute:: description

		**Type:** |nbsp| |nbsp| |nbsp| |nbsp| :py:obj:`~typing.Optional`\[:py:class:`str`\]

		A short description of the argument.
	"""

	def __init__(self, *args, description: Optional[str] = None, **kwargs):
		super().__init__(*args, **kwargs)

		self.description: Optional[str] = description
