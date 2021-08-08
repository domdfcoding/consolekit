###########
consolekit
###########

.. start short_desc

**Additional utilities for click.**

.. end short_desc

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/consolekit/latest?logo=read-the-docs
	:target: https://consolekit.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/consolekit/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/consolekit/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/consolekit/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/consolekit/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/consolekit/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/consolekit/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/consolekit/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/consolekit/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/consolekit/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/consolekit/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/consolekit/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/consolekit/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

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

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/consolekit/v1.3.0
	:target: https://github.com/domdfcoding/consolekit/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/consolekit
	:target: https://github.com/domdfcoding/consolekit/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/consolekit
	:target: https://pypi.org/project/consolekit/
	:alt: PyPI - Downloads

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

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install consolekit

.. end installation

Additionally, for better support in terminals,
install `psutil <https://pypi.org/project/psutil/>`_ by specifying the ``terminals`` extra:

.. code-block:: bash

	$ python -m pip install consolekit[terminals]

or, if you installed ``consolekit`` through conda:

.. code-block:: bash

	$ conda install -c conda-forge psutil
