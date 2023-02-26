#!/bin/bash

es

cd $TEST_DATA_DIR
git checkout data

cp -r /tmp/news_lk3_data/* $TEST_DATA_DIR/

git add .
git commit -m "Updated data"

git push origin data

