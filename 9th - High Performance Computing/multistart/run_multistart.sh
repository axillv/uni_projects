#!/usr/bin/env bash
set -euo pipefail
export BASH_ENV=

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

MODE=${MODE:-seq}            # seq|omp|omp_task|mpi
CONCURRENCY=${CONCURRENCY:-4}
MPIEXEC=${MPIEXEC:-mpiexec}
MPI_ENV_ENABLE=${MPI_ENV_ENABLE:-auto}
MPI_ENV_SCRIPT=${MPI_ENV_SCRIPT:-"$PROJECT_ROOT/setup_mpi_env.sh"}
LOG_PREFIX=${LOG_PREFIX:-ms}
LOGDIR=${LOGDIR:-"$SCRIPT_DIR/logs"}

BIN_SEQ=${BIN_SEQ:-"$SCRIPT_DIR/multistart_mds_seq"}
BIN_OMP=${BIN_OMP:-"$SCRIPT_DIR/multistart_mds_omp"}
BIN_OMP_TASK=${BIN_OMP_TASK:-"$SCRIPT_DIR/multistart_mds_omp_task"}
BIN_MPI=${BIN_MPI:-"$SCRIPT_DIR/multistart_mds_mpi"}

usage() {
  cat <<EOF
Usage: $0 [-m MODE] [-c CONCURRENCY] [-e MPIEXEC] [-p LOG_PREFIX]

MODE options: seq, omp, omp_task, mpi
CONCURRENCY: threads (omp/omp_task) or ranks (mpi). Ignored for seq.
Env knobs: LOG_ROOT, LOGDIR, MPI_ENV_ENABLE, MPI_ENV_SCRIPT, BIN_* overrides.
EOF
}

while getopts ":m:c:e:p:h" opt; do
  case $opt in
    m) MODE=${OPTARG} ;;
    c) CONCURRENCY=${OPTARG} ;;
    e) MPIEXEC=${OPTARG} ;;
    p) LOG_PREFIX=${OPTARG} ;;
    h) usage; exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2; usage; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2; usage; exit 1 ;;
  esac
done
shift $((OPTIND -1))

mkdir -p "$LOGDIR"

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

require_exec() {
  if [[ ! -x "$1" ]]; then
    echo "Executable missing: $1" >&2
    echo "Build with: make -C $SCRIPT_DIR" >&2
    exit 2
  fi
}

run_cmd() {
  local logfile
  local stamp
  stamp=$(date +%Y%m%d_%H%M%S)
  logfile="$LOGDIR/${LOG_PREFIX}_${MODE}_c${CONCURRENCY}_${stamp}.log"
  echo "Logging to: $logfile"
  "$@" 2>&1 | tee "$logfile"
  return ${PIPESTATUS[0]}
}

case "$MODE" in
  seq)
    CONCURRENCY=1
    require_exec "$BIN_SEQ"
    echo "Running sequential"
    run_cmd "$BIN_SEQ"
    ;;
  omp)
    require_exec "$BIN_OMP"
    echo "Running OpenMP with OMP_NUM_THREADS=$CONCURRENCY"
    OMP_NUM_THREADS=$CONCURRENCY run_cmd "$BIN_OMP"
    ;;
  omp_task)
    require_exec "$BIN_OMP_TASK"
    echo "Running OpenMP tasks with OMP_NUM_THREADS=$CONCURRENCY"
    OMP_NUM_THREADS=$CONCURRENCY run_cmd "$BIN_OMP_TASK"
    ;;
  mpi)
    require_exec "$BIN_MPI"
    maybe_source_mpi_env || true
    if ! command -v "$MPIEXEC" >/dev/null 2>&1 && ! command -v mpirun >/dev/null 2>&1; then
      echo "MPI launcher not found (MPIEXEC=$MPIEXEC)." >&2
      exit 3
    fi
    echo "Running MPI with $CONCURRENCY ranks"
    run_cmd "$MPIEXEC" -n "$CONCURRENCY" "$BIN_MPI"
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    usage
    exit 1
    ;;
esac