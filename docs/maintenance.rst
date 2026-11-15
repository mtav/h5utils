================
Maintainer infos
================

Packages to install for maintainance/development
================================================
* bumpversion
* tox
* ruff
* pylint

Releasing a new version:
========================

.. code:: bash

	bash ./packaging/release.sh

Documentation update:
=====================

The documentations are automatically updated on https://h5utils.readthedocs.io/.
If you want to generate it locally, run one of the make commands in docs/ as follows:

.. code:: bash

        cd ./docs
        # clean up
        make clean
        # documentation without todo notes
        make html-without-todo
        # documentation with todo notes
        make html-with-todo
        # make documentation with and without todo notes
        make all

Or for convenience:

.. code:: bash

        bash ./packaging/update_docs.sh

Configuration files of interest:
================================

* *pyproject.toml* : packaging (setuptools) configuration and version
* *./docs/conf.py* : sphinx configuration
* *tox.ini* : for testing with tox
* *.bumpversion.cfg* : bumpversion configuration
* *.pylintrc* : pylint configuration
* *~/.pypirc* : credentials to upload to PyPi

Running tests, linting and code formatting
==========================================

.. code:: bash

        # Directly, with unittest
        python3 -m unittest discover -s tests -v
        # With pytest
        pip install pytest
        pytest tests -v
        # With tox
        tox                  # all environments
        tox -e 3.12          # one Python version
        tox -e lint          # ruff only
        tox -e 3.12 -- -k test_2D_conversion -v   # pass pytest options after --
        # Linting and code formatting
        ruff check
        pylint ./h5utils/

Help with ruff:
===============

.. code:: bash

        # Select specific rules/files/folders
        ruff check --select UP008
        ruff check --select UP008 --fix
        ruff check --select UP008,UP004 --fix h5utils/h5utils.py
        ruff check --select UP008,UP004 --fix h5utils/

        # Preview the safe fixes as a diff, changing nothing
        ruff check --diff .

        # Apply only the safe fixes
        ruff check --fix .

        # List which violations are safely fixable
        # The marker [*] in Ruff’s output means “safe fix available”. Unsafe fixes appear only when you add --unsafe-fixes.
        ruff check --output-format=concise . | grep '\[\*\]'

        # Count fixable rules at a glance
        ruff check --statistics .

        # Preview the unsafe fixes as well
        ruff check --diff --unsafe-fixes .

TODO
====
* Fix pylint and ruff warnings.
* Document and test/fix scripts in packaging/
* Fix tox run.
* Test and document 2D support.
* Update docs and make new relase with 2D support.
* Add array creation. (like mpb-data -x -y -z)
* Add rectangular cell output. (like mpb-data -r)
* Replace constants module with scipy.constants.
* Add examples/tests/documentation for BFDTD support.
