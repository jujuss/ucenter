#!/usr/bin/env bash

date=`date +"%Y%m%d_%H%M%S"`
tar -zcvf ucenter.tar.gz --exclude=.git/ .
