#!/usr/bin/env python3
#
#  testing.py
"""
Test helpers.

.. versionadded:: 0.9.0

.. extras-require:: testing
	:pyproject:
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
#  Result and CliRunner based on https://github.com/pallets/click
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
from types import TracebackType
from typing import IO, Any, Iterable, Mapping, Optional, Tuple, Type, Union

# 3rd party
import click.testing
import pytest  # nodep
from coincidence.regressions import check_file_regression  # nodep
from pytest_regressions.file_regression import FileRegressionFixture  # nodep
from typing_extensions import Literal

__all__ = ["CliRunner", "Result", "cli_runner"]

_click_major = int(click.__version__.split('.')[0])


class Result(click.testing.Result):
	"""
	Holds the captured result of an invoked CLI script.

	:param runner: The runner that created the result.
	:param stdout_bytes: The standard output as bytes.
	:param stderr_bytes: The standard error as bytes, or :py:obj:`None` if not available.
	:param exit_code: The command's exit code.
	:param exception: The exception that occurred, if any.
	:param exc_info: The traceback, if an exception occurred.
	"""

	runner: click.testing.CliRunner
	exit_code: int
	exception: Optional[BaseException]
	exc_info: Optional[Any]
	stdout_bytes: bytes
	stderr_bytes: Optional[bytes]
	return_value: Optional[Tuple[Type[BaseException], BaseException, TracebackType]]

	def __init__(
			self,
			runner: click.testing.CliRunner,
			stdout_bytes: bytes,
			stderr_bytes: Optional[bytes],
			exit_code: int,
			exception: Optional[BaseException],
			exc_info: Optional[Tuple[Type[BaseException], BaseException, TracebackType]] = None,
			) -> None:

		if _click_major >= 8:
			super().__init__(
					runner=runner,
					stdout_bytes=stdout_bytes,
					stderr_bytes=stderr_bytes,
					exit_code=exit_code,
					exception=exception,
					exc_info=exc_info,
					return_value=None,
					)
		else:
			super().__init__(  # type: ignore
				runner=runner,
				stdout_bytes=stdout_bytes,
				stderr_bytes=stderr_bytes,
				exit_code=exit_code,
				exception=exception,
				exc_info=exc_info,
				)

	@property
	def output(self) -> str:
		"""
		The (standard) output as a string.
		"""

		return super().output

	@property
	def stdout(self) -> str:
		"""
		The standard output as a string.
		"""

		return super().stdout

	@property
	def stderr(self) -> str:
		"""
		The standard error as a string.
		"""

		return super().stderr

	@classmethod
	def _from_click_result(cls, result: click.testing.Result):
		return cls(
				runner=result.runner,
				stdout_bytes=result.stdout_bytes,
				stderr_bytes=result.stderr_bytes,
				exit_code=result.exit_code,
				exception=result.exception,
				exc_info=result.exc_info,
				)

	def check_stdout(
			self,
			file_regression: FileRegressionFixture,
			extension: str = ".txt",
			**kwargs,
			) -> Literal[True]:
		r"""
		Perform a regression check on the standard output from the command.

		:param file_regression:
		:param extension: The extension of the reference file.
		:param \*\*kwargs: Additional keyword arguments passed to :meth:`.FileRegressionFixture.check`.
		"""

		__tracebackhide__ = True

		check_file_regression(self.stdout.rstrip(), file_regression, extension=extension, **kwargs)

		return True


class CliRunner(click.testing.CliRunner):
	"""
	Provides functionality to invoke and test a Click script in an isolated environment.

	This only works in single-threaded systems without any concurrency as it changes the global interpreter state.

	:param charset: The character set for the input and output data.
	:param env: A dictionary with environment variables to override.
	:param echo_stdin: If :py:obj:`True`, then reading from stdin writes to stdout.
		This is useful for showing examples in some circumstances.
		Note that regular prompts will automatically echo the input.
	:param mix_stderr: If :py:obj:`False`, then stdout and stderr are preserved as independent streams.
		This is useful for Unix-philosophy apps that have predictable stdout and noisy stderr,
		such that each may be measured independently.

	.. autoclasssumm:: CliRunner
		:autosummary-sections: ;;
	"""

	def __init__(
			self,
			charset: str = "UTF-8",
			env: Optional[Mapping[str, str]] = None,
			*,
			echo_stdin: bool = False,
			mix_stderr: bool = True,
			) -> None:
		super().__init__(charset, env, echo_stdin, mix_stderr)

	def invoke(  # type: ignore  # noqa: D101
		self,
		cli: click.BaseCommand,
		args: Optional[Union[str, Iterable[str]]] = None,
		input: Optional[Union[bytes, str, IO]] = None,  # noqa: A002  # pylint: disable=redefined-builtin
		env: Optional[Mapping[str, str]] = None,
		*,
		catch_exceptions: bool = False,
		color: bool = False,
		**extra,
		) -> Result:
		r"""
		Invokes a command in an isolated environment.

		The arguments are forwarded directly to the command line script,
		the ``extra`` keyword arguments are passed to the :meth:`~click.Command.main`
		function of the command.

		:param cli: The command to invoke.
		:param args: The arguments to invoke. It may be given as an iterable or a string.
			When given as string it will be interpreted as a Unix shell command.
			More details at :func:`shlex.split`.
		:param input: The input data for ``sys.stdin``.
		:param env: The environment overrides.
		:param catch_exceptions: Whether to catch any other exceptions than :exc:`SystemExit`.
		:param color: whether the output should contain color codes.
			The application can still override this explicitly.
		:param \*\*extra: The keyword arguments to pass to :meth:`click.Command.main`.
		"""

		if args is not None and not isinstance(args, str):
			args = list(args)

		result = super().invoke(
				cli,
				args=args,
				input=input,
				env=env,
				catch_exceptions=catch_exceptions,
				color=color,
				**extra,
				)

		return Result._from_click_result(result)


@pytest.fixture()
def cli_runner() -> CliRunner:
	"""
	Returns a click runner for this test function.
	"""

	return CliRunner()
