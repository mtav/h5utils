#!/bin/bash
#WD=$(dirname ${0})

set -eu

ORIGDIR=$(readlink -f "$(dirname ${0})/..")
echo "ORIGDIR: ${ORIGDIR}"

cd ${ORIGDIR}
echo "==> pwd: $(pwd)"

NAME=$(grep -m1 '^name' pyproject.toml | cut -d'"' -f2)
CURRENT_VERSION=$(grep -m1 '^version' pyproject.toml | cut -d'"' -f2)

VENVDIR=/tmp/testdir/testenv

python3 -m build
# source testenv/bin/activate
source ${VENVDIR}/bin/activate
unset PYTHONPATH PYTHONSTARTUP
# pip uninstall ${NAME}
# pip install --force-reinstall --upgrade ${ORIGDIR}/dist/${NAME}-${CURRENT_VERSION}-py3-none-any.whl
pip install --upgrade --force-reinstall "${ORIGDIR}/dist/${NAME}-${CURRENT_VERSION}-py3-none-any.whl"
# find ${VENVDIR}/lib/python3.8/site-packages/
cat "${VENVDIR}"/lib/python*/site-packages/"${NAME}-${CURRENT_VERSION}.dist-info/RECORD"
