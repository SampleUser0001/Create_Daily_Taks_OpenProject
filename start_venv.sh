#!/bin/bash

source venv/bin/activate

pushd app > /dev/null
# 引数の数に応じて変更する
# bash start.sh $2 $3 ...
bash start.sh $1

popd > /dev/null

deactivate