#!/usr/bin/env bash
set -e
conda env create -f env_conda/mytools.yml
conda activate mytools
pip install -r env_conda/mytools_pip_env.txt
