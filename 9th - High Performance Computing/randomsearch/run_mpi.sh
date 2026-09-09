#!/usr/bin/env bash
set -euo pipefail
export BASH_ENV=

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Core knobs
RS_APP=${RS_APP:-"$SCRIPT_DIR/rs.py"}
PYTHON=${PYTHON:-"$(command -v python)"}
MPIEXEC=${MPIEXEC:-mpiexec}
MPI_ENV_ENABLE=${MPI_ENV_ENABLE:-auto} # auto|0|1
MPI_ENV_SCRIPT=${MPI_ENV_SCRIPT:-"$PROJECT_ROOT/setup_mpi_env.sh"}
CONDA_ENV=${CONDA_ENV:-"rs_env"}

# Centralized logging (per-project)
LOGDIR=${LOGDIR:-"$SCRIPT_DIR/logs"}

MODE=serial
WORKERS=4
MPI_PROCS=4
N_TRIALS=32
OUT_PREFIX=timings
DATASET_SEED=42

usage() {
  cat <<EOF
Usage: $0 [-m MODE] [-w WORKERS] [-n MPI_PROCS] [-t N_TRIALS] [-o OUT_PREFIX] [-s DATASET_SEED]

Modes: serial, threads, processes, mpi_futures, mpi_manual, all
Env overrides: RS_APP, PYTHON, MPIEXEC, LOGDIR
EOF
}

while getopts ":m:w:n:t:o:s:h" opt; do
  case ${opt} in
    m ) MODE=${OPTARG} ;;
    w ) WORKERS=${OPTARG} ;;
    n ) MPI_PROCS=${OPTARG} ;;
    t ) N_TRIALS=${OPTARG} ;;
    o ) OUT_PREFIX=${OPTARG} ;;
    s ) DATASET_SEED=${OPTARG} ;;
  esac
done
shift $((OPTIND -1))

if [[ "$MPI_PROCS" -lt 1 ]]; then
  echo "MPI_PROCS must be >=1" >&2
  exit 1
fi

mkdir -p "$LOGDIR"

activate_conda_env() {
  # Best-effort activation of the requested conda environment.
  # Falls back silently to current Python if conda or env is unavailable.
  if command -v conda >/dev/null 2>&1; then
    local conda_base
    conda_base=$(conda info --base 2>/dev/null || true)
    if [[ -n "$conda_base" && -f "$conda_base/etc/profile.d/conda.sh" ]]; then
      # shellcheck disable=SC1091
      set +u
      . "$conda_base/etc/profile.d/conda.sh"
      set -u
      if conda env list 2>/dev/null | awk '{print $1}' | grep -Fxq "$CONDA_ENV"; then
        conda activate "$CONDA_ENV" >/dev/null 2>&1 || true
        PYTHON=$(command -v python)
        echo "Using conda env $CONDA_ENV (python=$PYTHON)"
        return 0
      else
        echo "Conda env $CONDA_ENV not found; using PYTHON=$PYTHON" >&2
      fi
    fi
  else
    echo "conda command not found; using PYTHON=$PYTHON" >&2
  fi
  return 0
}

mpi_available() {
  command -v "$MPIEXEC" >/dev/null 2>&1 || command -v mpirun >/dev/null 2>&1 || command -v mpicc >/dev/null 2>&1
}

mpi_python_available() {
  "$PYTHON" - <<'PY' >/dev/null 2>&1
try:
    import mpi4py  # noqa: F401
    from mpi4py import futures  # noqa: F401
except Exception:
    raise SystemExit(1)
PY
}

# Optional environment hook for MPI stacks (e.g., Intel oneAPI setvars.sh).
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

activate_conda_env || true

run_cmd() {
  local cmd="$*"
  local stamp
  stamp=$(date +%Y%m%d_%H%M%S)
  local logfile="$LOGDIR/${OUT_PREFIX}_${MODE}_${stamp}.log"
  echo "Running: $cmd"
  echo "Logging to: $logfile"
  BASH_ENV= bash -c "$cmd" 2>&1 | tee "$logfile"
}

run_mode() {
  local m=$1
  maybe_source_mpi_env || true
  case $m in
    serial)
      cmd="$PYTHON \"$RS_APP\" --mode serial --n_trials $N_TRIALS --dataset-seed $DATASET_SEED"
      ;;
    threads)
      cmd="$PYTHON \"$RS_APP\" --mode threads --n_trials $N_TRIALS --workers $WORKERS --dataset-seed $DATASET_SEED"
      ;;
    processes)
      cmd="$PYTHON \"$RS_APP\" --mode processes --n_trials $N_TRIALS --workers $WORKERS --dataset-seed $DATASET_SEED"
      ;;
    mpi_futures)
      if ! mpi_available; then
        echo "MPI executables not found; cannot run mpi_futures" >&2
        return 2
      fi
      if ! mpi_python_available; then
        echo "Python MPI dependencies (mpi4py, mpi4py.futures) not available; cannot run mpi_futures" >&2
        return 2
      fi
      cmd="$MPIEXEC -n $MPI_PROCS $PYTHON \"$RS_APP\" --mode mpi_futures --n_trials $N_TRIALS --dataset-seed $DATASET_SEED"
      ;;
    mpi_manual)
      if ! mpi_available; then
        echo "MPI executables not found; cannot run mpi_manual" >&2
        return 2
      fi
      if ! mpi_python_available; then
        echo "Python MPI dependency (mpi4py) not available; cannot run mpi_manual" >&2
        return 2
      fi
      cmd="$MPIEXEC -n $MPI_PROCS $PYTHON \"$RS_APP\" --mode mpi_manual --n_trials $N_TRIALS --dataset-seed $DATASET_SEED"
      ;;
    *)
      echo "Unknown mode: $m" >&2; return 2 ;;
  esac
  run_cmd "$cmd"
}

if [ "$MODE" = "all" ]; then
  for m in serial threads processes mpi_futures mpi_manual; do
    MODE=$m run_mode "$m" || true
  done
else
  run_mode "$MODE"
fi

exit 0
