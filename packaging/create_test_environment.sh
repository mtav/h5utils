#!/bin/bash
# set -eu

# TESTDIR=${1:-$(mktemp --directory)}
TESTDIR=${1:-/tmp/testdir}
PKGDIR=$(readlink --canonicalize $(dirname ${0})/..)
echo "==> TESTDIR: ${TESTDIR}"
echo "==> PKGDIR: ${PKGDIR}"

# build package
cd ${PKGDIR}
NAME=$(grep -m1 '^name' pyproject.toml | cut -d'"' -f2)
CURRENT_VERSION=$(grep -m1 '^version' pyproject.toml | cut -d'"' -f2)
python3 -m build

# cd into testdir
mkdir --parents ${TESTDIR}
cd ${TESTDIR}

# activate virtualenv
# virtualenv testenv
virtualenv --clear testenv
source testenv/bin/activate
unset PYTHONPATH PYTHONSTARTUP

# install package
pip install --upgrade ${PKGDIR}/dist/${NAME}-${CURRENT_VERSION}-py3-none-any.whl
