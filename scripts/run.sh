#!/usr/bin/bash
set -o errexit
set -o nounset
set -o pipefail

function exists() {
  command -v "${@}" > /dev/null 2>&1
}

function info() {
  if exists rich; then
    rich --print --style "bold bright_blue" "${*}"
  else
    echo -e -n "\x1b[1;94m"
    echo -n "${*}"
    echo -e "\x1b[0m"
  fi
}

function call() {
  info "+ ${*}"
  "${@}"
}

call python -m wfiuh curve-fitting --input-dir "2-sub-WFIUH_rescaled" --output-dir "results/cdf/params" --func "cdf"
echo
call python -m wfiuh param-dis --input-dir "results/cdf/params" --output-dir "results/cdf/param-dis"
call python -m wfiuh curve-fitting --input-dir "2-sub-WFIUH_rescaled" --output-dir "results/pdf/params" --func "pdf"
echo
call python -m wfiuh param-dis --input-dir "results/pdf/params" --output-dir "results/pdf/param-dis"
