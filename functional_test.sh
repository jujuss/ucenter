#!/usr/bin/env bash

set -e

# # start service
python app.py &
pid=$!

# run functional tests
pytest .

# stop service
kill -TERM $pid
