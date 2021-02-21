================
Maintainer infos
================

Releasing a new version:
========================

.. code:: bash

	./packaging/release.sh

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

        ./packaging/update_docs.sh

Configuration files of interest:
================================

* *setup.py* : setuptools configuration
* *./docs/conf.py* : sphinx configuration
* *tox.ini* : for testing with tox
* *.bumpversion.cfg* : bumpversion configuration
* *.pylintrc* : pylint configuration
* *~/.pypirc* : credentials to upload to PyPi
