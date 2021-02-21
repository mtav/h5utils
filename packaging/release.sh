#!/bin/bash
set -eu

ORIGDIR=$(readlink -f "$(dirname ${0})/..")
echo "ORIGDIR: ${ORIGDIR}"
cd ${ORIGDIR}
echo "==> pwd: $(pwd)"

NAME=$(python3 setup.py --name)
CURRENT_VERSION=$(python3 setup.py --version)

# bump version
echo "bump version? (y:yes,n:no,q:quit)"
read ans
case $ans in
  y|Y|yes) bumpversion --verbose patch;;
  q) exit;;
  *) echo "keeping version=${CURRENT_VERSION}";;
esac

# bumpversion --current-version ${CURRENT_VERSION} patch setup.py
# bumpversion --verbose patch

# remove previous versions to avoid issues
rm -iv dist/*

# build package
python3 -m build

# upload
twine upload dist/*
