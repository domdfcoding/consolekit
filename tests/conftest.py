# stdlib
import os
from pathlib import Path

# 3rd party
import pytest
from domdf_python_tools.paths import PathPlus

pytest_plugins = ("coincidence", "consolekit.testing")


@pytest.fixture()
def original_datadir(request) -> Path:  # noqa: D103
	# Work around pycharm confusing datadir with test file.
	return PathPlus(os.path.splitext(request.module.__file__)[0] + '_')
