#!/bin/bash
set -eu

ORIGDIR=$(readlink -f "$(dirname ${0})/..")
echo "ORIGDIR: ${ORIGDIR}"
cd ${ORIGDIR}
echo "==> pwd: $(pwd)"

NAME=$(grep -m1 '^name' pyproject.toml | cut -d'"' -f2)
CURRENT_VERSION=$(grep -m1 '^version' pyproject.toml | cut -d'"' -f2)

# bump version
echo "bump version? (y:yes,n:no,q:quit)"
read ans
case $ans in
  y|Y|yes) bumpversion --verbose patch;;
  q) exit;;
  *) echo "keeping version=${CURRENT_VERSION}";;
esac

# bumpversion --current-version ${CURRENT_VERSION} patch pyproject.toml
# bumpversion --verbose patch

# remove previous versions to avoid issues
rm -iv dist/*

# build package
python3 -m build

# upload
twine upload dist/*
