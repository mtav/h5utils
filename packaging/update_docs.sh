#!/bin/bash
cd $(dirname ${0})/../docs
sphinx-apidoc -o source/ ../h5utils/
make clean all
