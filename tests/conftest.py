pytest_plugins = ("coincidence", "consolekit.testing")

try:
	# 3rd party
	import pytest_mypy_plugins.collect  # type: ignore
	from pytest_mypy_plugins.collect import YamlTestFile, pytest_addoption

	def pytest_collect_file(path, parent):
		if path.ext == ".yaml" and path.basename.startswith(("test-", "test_")):
			return YamlTestFile.from_parent(parent, fspath=path)
		return None

except ImportError:
	pass
