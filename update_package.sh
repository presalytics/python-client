#!/bin/bash

# Script requires a version number as first argument and a quoted commit message as 2nd argument

if [ -z "$1" ]
  then
    echo "No version number argument supplied"
    exit 2
fi

if [ -z "$2" ]
  then
    echo "No commit message argument supplied"
    exit 2
fi

# incorporate env file from parent directory
source ./../.env

set -exv

rm -r -f build dist presalytics.egg-info presalytics.log token.json
EXPRESSION='s/VERSION = "[0-9]+\.[0-9]+\.[0-9]+"/VERSION = "'$1'"/g'
sed -i -r "$EXPRESSION" setup.py
git add -u
git commit -m "$2"
python3 setup.py sdist bdist_wheel
twine upload dist/*
rm -r -f build dist presalytics.egg-info
git push origin master 

