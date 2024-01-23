#!/bin/bash
# install_and_freeze.sh

pip install "$@"
pip freeze > requirements.txt
