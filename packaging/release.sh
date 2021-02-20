#!/bin/bash
set -eu

ORIGDIR=$(readlink -f "$(dirname ${0})/..")
echo "ORIGDIR: ${ORIGDIR}"
cd ${ORIGDIR}
echo "==> pwd: $(pwd)"

NAME=$(python3 setup.py --name)
CURRENT_VERSION=$(python3 setup.py --version)

# bump version
bumpversion --current-version ${CURRENT_VERSION} patch setup.py

# remove previous versions to avoid issues
rm -iv dist/*

# build package
python3 -m build

# upload
twine upload dist/*
