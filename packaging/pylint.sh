#!/bin/bash
cd $(dirname ${0})/..
# pylint h5utils/h5tovts.py
pylint setup.py h5utils/
