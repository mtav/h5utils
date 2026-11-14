#!/bin/bash
set -eu

# cd into project directory
cd $(dirname ${0})/..
echo "==> pwd: $(pwd)"

# build and upload to test pypi
CURRENT_VERSION=$(grep -m1 '^version' pyproject.toml | cut -d'"' -f2)
NAME=$(grep -m1 '^name' pyproject.toml | cut -d'"' -f2)
echo "==> CURRENT_VERSION=${CURRENT_VERSION}"
# bumpversion --current-version ${CURRENT_VERSION} patch pyproject.toml
rm -rf build
# rm -iv dist/*
python3 -m build
# python3 -m twine upload --repository testpypi dist/*

# check requirements
pkginfo -f requires_dist dist/${NAME}-*.whl

# test package
bash ./packaging/package_test.sh dist/${NAME}-*.whl
