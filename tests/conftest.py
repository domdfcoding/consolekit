# stdlib
from typing import Optional

pytest_plugins = ("coincidence", "consolekit.testing")

try:
	# 3rd party
	from pytest_mypy_plugins.collect import YamlTestFile, pytest_addoption  # noqa: F401

	def pytest_collect_file(file_path, parent) -> Optional[YamlTestFile]:  # noqa: MAN001
		if file_path.suffix == ".yaml" and file_path.name.startswith(("test-", "test_")):
			return YamlTestFile.from_parent(parent, path=file_path, fspath=None)
		return None

except ImportError:
	pass
