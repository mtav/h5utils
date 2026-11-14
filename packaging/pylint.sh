#!/bin/bash
cd $(dirname ${0})/..
# pylint h5utils/h5tovts.py
# pylint h5utils/
# pylint --disable=all --enable=trailing-whitespace h5utils/h5utils.py
# pylint --disable=all --enable=trailing-whitespace h5utils/
pylint --disable=all --enable=missing-function-docstring --enable=missing-module-docstring h5utils/
