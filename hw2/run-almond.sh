#!/bin/bash

set -e
set -o pipefail
set -x

export THINGENGINE_HOME=${PWD}/home
export THINGENGINE_NLP_URL=http://127.0.0.1:8400
exec node ./almond-server/main.js
