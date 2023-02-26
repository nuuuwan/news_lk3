#!/bin/bash

cp -r /tmp/news_lk3_data/* .

git add .
git commit -m "Updated data"

git push origin data
