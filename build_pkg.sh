#!/usr/bin/env bash

date=`date +"%Y%m%d_%H%M%S"`
echo ${TRAVIS_TAG}
tar -zcvf ucenter-${TRAVIS_TAG}.tar.gz --exclude=.git/ .
