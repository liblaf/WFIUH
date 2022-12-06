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

call python -m wfiuh curve-fitting --input-dir "2-sub-WFIUH_rescaled" --output-dir "results/params/cdf" --func "cdf"
echo
call python -m wfiuh param-dis --input-dir "results/params/cdf" --output-dir "results/param-dis/cdf" --threshold 0.9
call python -m wfiuh curve-fitting --input-dir "2-sub-WFIUH_rescaled" --output-dir "results/params/pdf" --func "pdf"
echo
call python -m wfiuh param-dis --input-dir "results/params/pdf" --output-dir "results/param-dis/pdf" --threshold 0.9
