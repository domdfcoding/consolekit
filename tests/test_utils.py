# stdlib
import sys

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.testing import check_file_regression
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from consolekit.utils import coloured_diff, overtype


def test_overtype(capsys):
	print("Waiting...", end='')
	overtype("foo", "bar")
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Waiting...\rfoo bar"]

	print("Waiting...", end='')
	overtype("foo", "bar", sep='')
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Waiting...\rfoobar"]

	print("Waiting...", end='')
	overtype("foo", "bar", sep='-', end='\n')
	sys.stdout.flush()

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout == ["Waiting...\rfoo-bar", '']

	sys.stderr.write("Waiting...")
	overtype("foo", "bar", file=sys.stderr)
	sys.stdout.flush()

	captured = capsys.readouterr()
	stderr = captured.err.split('\n')
	assert stderr == ["Waiting...\rfoo bar"]


def test_coloured_diff(file_regression: FileRegressionFixture):
	data_dir = PathPlus(__file__).parent / "test_diff_"
	original = data_dir / "original"
	modified = data_dir / "modified"

	diff = coloured_diff(
			original.read_lines(),
			modified.read_lines(),
			fromfile="original_file.txt",
			tofile="modified_file.txt",
			fromfiledate="(original)",
			tofiledate="(modified)",
			lineterm='',
			)

	check_file_regression(diff, file_regression)
