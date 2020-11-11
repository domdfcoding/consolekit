###########
consolekit
###########

.. start short_desc

**Additional utilities for click.**

.. end short_desc

Spun out from `repo_helper <https://github.com/domdfcoding/repo_helper>`_. Needs more tests.

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/consolekit/latest?logo=read-the-docs
	:target: https://consolekit.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/consolekit/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/consolekit/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/consolekit/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/consolekit
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/consolekit/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/consolekit/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/consolekit/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/consolekit/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/consolekit/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/consolekit/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/consolekit/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/consolekit?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/consolekit?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/consolekit
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/consolekit
	:target: https://pypi.org/project/consolekit/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/consolekit?logo=python&logoColor=white
	:target: https://pypi.org/project/consolekit/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/consolekit
	:target: https://pypi.org/project/consolekit/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/consolekit
	:target: https://pypi.org/project/consolekit/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/consolekit?logo=anaconda
	:target: https://anaconda.org/domdfcoding/consolekit
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/consolekit?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/consolekit
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/consolekit
	:target: https://github.com/domdfcoding/consolekit/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/consolekit
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/consolekit/v0.3.2
	:target: https://github.com/domdfcoding/consolekit/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/consolekit
	:target: https://github.com/domdfcoding/consolekit/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/consolekit/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/consolekit/master
	:alt: pre-commit.ci status

.. end shields

Installation
--------------

.. start installation

``consolekit`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install consolekit

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels http://conda.anaconda.org/domdfcoding
		$ conda config --add channels http://conda.anaconda.org/conda-forge

	* Then install

	.. code-block:: bash

		$ conda install consolekit

.. end installation
