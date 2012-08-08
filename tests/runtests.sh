#!/bin/bash

set -e

export PYTHONPATH=$PWD/..:$PYTHONPATH

django-admin.py test --settings=tests.settings_sites test_sites
django-admin.py test --settings=tests.settings_options test_options
