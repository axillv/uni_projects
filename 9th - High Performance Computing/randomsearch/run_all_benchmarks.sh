#!/usr/bin/env bash
set -euo pipefail
export BASH_ENV=

# Simple benchmark runner: executes run_mpi.sh across modes/concurrencies and
# writes a single CSV summary in this directory, logging centrally under the
# repository's logs folder.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RUN_MPI="$SCRIPT_DIR/run_mpi.sh"
SUMMARY_FILE="$SCRIPT_DIR/benchmarks_summary.csv"
MPIEXEC=${MPIEXEC:-mpiexec}
MPI_ENV_ENABLE=${MPI_ENV_ENABLE:-auto}
MPI_ENV_SCRIPT=${MPI_ENV_SCRIPT:-"$PROJECT_ROOT/setup_mpi_env.sh"}
CONDA_ENV=${CONDA_ENV:-"rs_env"}

LOGDIR=${LOGDIR:-"$SCRIPT_DIR/logs"}

NUM_TRIALS=${NUM_TRIALS:-48}
DATASET_SEED=${DATASET_SEED:-42}
CONCURRENCY_LIST=${CONCURRENCY_LIST:-"1,2,4,6,8,12,16"}
MODE_LIST=${MODE_LIST:-"serial,threads,processes,mpi_futures,mpi_manual"}

usage() {
  cat <<EOF
Usage: $0 [-t NUM_TRIALS] [-s DATASET_SEED] [-c CONCURRENCY_LIST] [-m MODE_LIST]

Defaults: NUM_TRIALS=$NUM_TRIALS DATASET_SEED=$DATASET_SEED
          CONCURRENCY_LIST=$CONCURRENCY_LIST MODE_LIST=$MODE_LIST
EOF
}

while getopts ":t:s:c:m:h" opt; do
  case $opt in
    t) NUM_TRIALS=${OPTARG} ;;
    s) DATASET_SEED=${OPTARG} ;;
    c) CONCURRENCY_LIST=${OPTARG} ;;
    m) MODE_LIST=${OPTARG} ;;
    h) usage; exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2; usage; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2; usage; exit 1 ;;
  esac
done
shift $((OPTIND -1))

IFS="," read -r -a CONCURRENCIES <<< "$CONCURRENCY_LIST"
IFS="," read -r -a MODES <<< "$MODE_LIST"

mkdir -p "$LOGDIR"

echo "mode,concurrency,total_seconds" > "$SUMMARY_FILE"

mpi_available() {
  command -v "$MPIEXEC" >/dev/null 2>&1 || command -v mpirun >/dev/null 2>&1 || command -v mpicc >/dev/null 2>&1
}

maybe_source_mpi_env() {
  if [[ "$MPI_ENV_ENABLE" =~ ^(0|false|off)$ ]]; then
    return 0
  fi
  if [[ -n "${MPI_ENV_SOURCED:-}" ]]; then
    return 0
  fi
  if [[ "$MPI_ENV_ENABLE" == "auto" && ! -f "$MPI_ENV_SCRIPT" ]]; then
    return 0
  fi
  if [[ ! -f "$MPI_ENV_SCRIPT" ]]; then
    echo "MPI env script $MPI_ENV_SCRIPT not found; skipping MPI env setup" >&2
    return 0
  fi
  echo "Sourcing MPI environment from $MPI_ENV_SCRIPT"
  # shellcheck disable=SC1090
  set +u
  . "$MPI_ENV_SCRIPT"
  set -u
  MPI_ENV_SOURCED=1
}

run_case() {
  local mode=$1
  local concurrency=$2
  local out_prefix="bench_${mode}_c${concurrency}"
  local cmd=("$RUN_MPI" "-m" "$mode" "-t" "$NUM_TRIALS" "-s" "$DATASET_SEED" "-o" "$out_prefix")

  if [[ "$mode" == "threads" || "$mode" == "processes" ]]; then
    cmd+=("-w" "$concurrency")
  elif [[ "$mode" == "mpi_futures" || "$mode" == "mpi_manual" ]]; then
    maybe_source_mpi_env || true
    if ! mpi_available; then
      echo "Skipping ${mode} (concurrency=${concurrency}) because MPI is not available even after MPI env setup"
      return 0
    fi
    cmd+=("-n" "$concurrency")
  fi

  echo "Running ${mode} (concurrency=${concurrency})"
  local output
  if ! output=$("${cmd[@]}" 2>&1 | tee /dev/tty); then
    echo "Command failed for mode=$mode concurrency=$concurrency" >&2
    exit 1
  fi

  local time_line
  time_line=$(echo "$output" | grep -E "completed in [0-9]+\.[0-9]+s" | tail -1 || true)
  if [[ -z "$time_line" ]]; then
    echo "Could not parse duration for $mode concurrency=$concurrency" >&2
    exit 1
  fi
  local secs
  secs=$(echo "$time_line" | grep -oE "[0-9]+\.[0-9]+" | head -n 1)
  echo "$mode,$concurrency,$secs" >> "$SUMMARY_FILE"
}

for mode in "${MODES[@]}"; do
  if [[ "$mode" == "serial" ]]; then
    workers=(1)
  else
    workers=("${CONCURRENCIES[@]}")
  fi
  for conc in "${workers[@]}"; do
    run_case "$mode" "$conc"
  done
done
