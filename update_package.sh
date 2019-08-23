#!/bin/bash

# Script requires a quoted commit message as an argument

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 2
fi

source ./../.env

set -exv

rm -r -f build dist presalytics.egg-info presalytics.log token.json
git add .
git commit -m "$1"
python3 setup.py sdist bdist_wheel
twine upload dist/*
git push origin master

