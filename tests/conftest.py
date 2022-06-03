# stdlib
from typing import Optional

pytest_plugins = ("coincidence", "consolekit.testing")

try:
	# 3rd party
	from pytest_mypy_plugins.collect import YamlTestFile, pytest_addoption  # noqa: F401

	def pytest_collect_file(path, parent) -> Optional[YamlTestFile]:  # noqa: MAN001
		if path.ext == ".yaml" and path.basename.startswith(("test-", "test_")):
			return YamlTestFile.from_parent(parent, fspath=path)
		return None

except ImportError:
	pass
