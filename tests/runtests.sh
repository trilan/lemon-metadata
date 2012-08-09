#!/bin/bash

set -e

export PYTHONPATH=$PWD/..:$PYTHONPATH

TYPES="sites options context_processors"

if [ $# -gt 0 ]; then
  TYPES=$@
fi

for type in $TYPES; do
  django-admin.py test --settings=tests.settings_$type test_$type
done
