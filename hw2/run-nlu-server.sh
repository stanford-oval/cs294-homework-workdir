#!/bin/bash

set -e
set -o pipefail

GENIE=${GENIE:-${PWD}/genie-toolkit/tool/genie.js}

. ./lib.sh
parse_args "$0" "experiment nlu_model" "$@"

set -x

make experiment="${experiment}" "${experiment}/models/${nlu_model}/best.pth"

export GENIE_TOKENIZER_ADDRESS=cs294s-tokenizer.almond.stanford.edu:8888
exec node --experimental_worker "${GENIE}" server \
  --locale en-US --port ${PORT:-8400} \
  --nlu-model "${experiment}/models/${nlu_model}" \
  --thingpedia "${experiment}/schema.tt" 
