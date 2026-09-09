#!/usr/bin/env bash
set -euo pipefail
export BASH_ENV=

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
RUNNER="$SCRIPT_DIR/run_multistart.sh"
SUMMARY_FILE="$SCRIPT_DIR/benchmarks_summary.csv"

CONCURRENCY_LIST=${CONCURRENCY_LIST:-"1,2,4,6,8,12,16"}
MODE_LIST=${MODE_LIST:-"seq,omp,omp_task,mpi"}
MPIEXEC=${MPIEXEC:-mpiexec}
MPI_ENV_ENABLE=${MPI_ENV_ENABLE:-auto}
MPI_ENV_SCRIPT=${MPI_ENV_SCRIPT:-"$PROJECT_ROOT/setup_mpi_env.sh"}
LOGDIR=${LOGDIR:-"$SCRIPT_DIR/logs"}

usage() {
  cat <<EOF
Usage: $0 [-c CONCURRENCY_LIST] [-m MODE_LIST]
Defaults: CONCURRENCY_LIST=$CONCURRENCY_LIST, MODE_LIST=$MODE_LIST
Env: MPIEXEC, MPI_ENV_ENABLE, LOG_ROOT, LOGDIR propagate to the runner.
EOF
}

while getopts ":c:m:h" opt; do
  case $opt in
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

mpi_available() {
  command -v "$MPIEXEC" >/dev/null 2>&1 || command -v mpirun >/dev/null 2>&1 || command -v mpicc >/dev/null 2>&1
}

build_binaries() {
  echo "Building multistart binaries..."
  make -C "$SCRIPT_DIR" -j multistart_mds_seq multistart_mds_omp multistart_mds_omp_task >/dev/null
  maybe_source_mpi_env || true
  if mpi_available; then
    make -C "$SCRIPT_DIR" -j multistart_mds_mpi >/dev/null
  else
    echo "Skipping MPI binary build (mpicc/mpiexec not detected)"
  fi
}

run_case() {
  local mode=$1
  local conc=$2
  local effective_conc=$conc

  if [[ "$mode" == "seq" ]]; then
    effective_conc=1
  fi

  if [[ "$mode" == "mpi" ]]; then
    maybe_source_mpi_env || true
    if ! mpi_available; then
      echo "Skipping MPI mode (concurrency=$conc) because MPI is unavailable"
      return 0
    fi
  fi

  local cmd=("$RUNNER" "-m" "$mode" "-c" "$effective_conc" "-e" "$MPIEXEC")
  echo "Running $mode (concurrency=$effective_conc)"

  local output
  if ! output=$(LOGDIR="$LOGDIR" MPI_ENV_ENABLE="$MPI_ENV_ENABLE" MPI_ENV_SCRIPT="$MPI_ENV_SCRIPT" "${cmd[@]}" 2>&1 | tee /dev/tty); then
    echo "Run failed for mode=$mode concurrency=$effective_conc" >&2
    exit 1
  fi

  local time_line
  time_line=$(echo "$output" | grep -E "Elapsed time = [0-9]+\.[0-9]+" | tail -1 || true)
  if [[ -z "$time_line" ]]; then
    echo "Could not parse elapsed time for $mode concurrency=$effective_conc" >&2
    exit 1
  fi
  local secs
  secs=$(echo "$time_line" | grep -oE "[0-9]+\.[0-9]+" | head -n 1)
  echo "$mode,$effective_conc,$secs" >> "$SUMMARY_FILE"
}

build_binaries

for mode in "${MODES[@]}"; do
  for conc in "${CONCURRENCIES[@]}"; do
    # Avoid redundant concurrency variants for seq
    if [[ "$mode" == "seq" && "$conc" != "1" ]]; then
      continue
    fi
    run_case "$mode" "$conc"
  done
done

echo "Benchmark CSV written to $SUMMARY_FILE"
