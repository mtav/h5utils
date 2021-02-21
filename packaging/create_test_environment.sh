#!/bin/bash
# set -eu

# TESTDIR=${1:-$(mktemp --directory)}
TESTDIR=${1:-/tmp/testdir}
PKGDIR=$(readlink --canonicalize $(dirname ${0})/..)
echo "==> TESTDIR: ${TESTDIR}"
echo "==> PKGDIR: ${PKGDIR}"

# build package
cd ${PKGDIR}
NAME=$(python3 setup.py --name)
CURRENT_VERSION=$(python3 setup.py --version)
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
