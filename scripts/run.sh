#!/usr/bin/bash
set -o errexit
set -o nounset
set -o pipefail

models=("Beta" "DoublePower" "DoubleTriangular" "Frechet" "Gamma" "Hill" "Hoerl" "InverseGaussian" "Kumaraswamy" "Logistic" "Multistage" "NormalGaussian" "Polynomial" "Rational" "ShiftedLogPearson3" "Weibull")

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

call python entry_point.py curve-fitting \
  --input-dir "2-sub-WFIUH_rescaled" \
  --output-dir "results/params/cdf" \
  --fit cdf
echo

call python entry_point.py curve-fitting \
  --input-dir "2-sub-WFIUH_rescaled" \
  --output-dir "results/params/pdf" \
  --fit pdf
echo

call python entry_point.py param-dis \
  --input-dir "results/params/cdf" \
  --output-dir "results/param-dis/cdf/cdf" \
  --key "cdf_r2_score" \
  --threshold 0.9

call python entry_point.py param-dis \
  --input-dir "results/params/cdf" \
  --output-dir "results/param-dis/cdf/pdf" \
  --key "pdf_r2_score" \
  --threshold 0.9

call python entry_point.py param-dis \
  --input-dir "results/params/pdf" \
  --output-dir "results/param-dis/pdf/cdf" \
  --key "cdf_r2_score" \
  --threshold 0.9

call python entry_point.py param-dis \
  --input-dir "results/params/pdf" \
  --output-dir "results/param-dis/pdf/pdf" \
  --key "pdf_r2_score" \
  --threshold 0.9

for model in "${models[@]}"; do
  call python entry_point.py best-sample \
    --model "${model}" \
    --param-path "results/params/cdf/${model}.csv" \
    --output "results/samples/${model}.png" \
    --threshold 0.9
done
