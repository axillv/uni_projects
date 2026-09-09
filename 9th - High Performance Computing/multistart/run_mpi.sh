#!/usr/bin/env bash
set -euo pipefail
export BASH_ENV=

# Simple MPI runner wrapper for this project
# Usage: run_mpi.sh [-n NPROCS] [-e MPIEXEC] [-a APP] [-- app-args...]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

MPI_PROCS=${MPI_PROCS:-4}
MPIEXEC=${MPIEXEC:-mpiexec}
MPI_ENV_ENABLE=${MPI_ENV_ENABLE:-auto}
MPI_ENV_SCRIPT=${MPI_ENV_SCRIPT:-"$PROJECT_ROOT/setup_mpi_env.sh"}
APP=${APP:-"$SCRIPT_DIR/multistart_mds_mpi"}
LOGDIR=${LOGDIR:-"$SCRIPT_DIR/logs"}

while getopts ":n:e:a:h" opt; do
  case ${opt} in
    n ) MPI_PROCS=${OPTARG} ;;
    e ) MPIEXEC=${OPTARG} ;;
    a ) APP=${OPTARG} ;;
    h )
      echo "Usage: $0 [-n NPROCS] [-e MPIEXEC] [-a APP] [-- app-args...]"
      echo
      echo "Defaults: MPI_PROCS=$MPI_PROCS, MPIEXEC=$MPIEXEC, APP=$APP"
      exit 0
      ;;
    \? ) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
    : ) echo "Option -$OPTARG requires an argument." >&2; exit 1 ;;
  esac
done
shift $((OPTIND -1))

if [[ "$MPI_PROCS" -lt 1 ]]; then
  echo "MPI_PROCS must be >=1" >&2
  exit 1
fi

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

maybe_source_mpi_env || true

if [ ! -x "$APP" ]; then
  echo "Executable $APP not found or not executable." >&2
  echo "Build first: make multistart_mds_mpi" >&2
  exit 2
fi

mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/run_mpi_$(date +%Y%m%d_%H%M%S).log"

echo "Running MPI app with: $MPIEXEC -n $MPI_PROCS $APP $*"
echo "Logging to: $LOGFILE"
"$MPIEXEC" -n "$MPI_PROCS" "$APP" "$@" 2>&1 | tee "$LOGFILE"
exit ${PIPESTATUS[0]}
