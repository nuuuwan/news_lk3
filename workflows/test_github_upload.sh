#!/bin/bash

GIT_REPO=https://github.com/nuuuwan/news_lk3_data.git
TEST_DATA_DIR=/tmp/news_lk3_data-test

rm -rf $TEST_DATA_DIR
mkdir $TEST_DATA_DIR
git clone $GIT_REPO $TEST_DATA_DIR

cd $TEST_DATA_DIR

cp -r /tmp/news_lk3_data/* $TEST_DATA_DIR/

git add .
git commit -m "Updated data"

git push origin main

