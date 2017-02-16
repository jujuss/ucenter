#!/usr/bin/env bash

echo ${TRAVIS_TAG}
tar -zcvf ucenter-${TRAVIS_TAG}.tar.gz --exclude="./.git" --exclude="./.gitignore" *
