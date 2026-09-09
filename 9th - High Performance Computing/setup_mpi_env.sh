#!/usr/bin/env bash
# Shared MPI environment bootstrapper for both randomsearch (Python) and multistart (C).
# Safe to source multiple times; does nothing if MPI_ENV_ENABLE is false/off.
#
# Controls:
#   MPI_ENV_ENABLE=auto|1|0  (default: auto)
#   MPI_ENV_SCRIPT=</custom/script> to override this file from callers
#   ONEAPI_SET_VARS=/opt/intel/oneapi/setvars.sh (override path if different)
#   MPIEXEC override to select a specific launcher
#
# Usage: source this file before running MPI binaries if your MPI stack requires setup.

# Prevent repeated work in a single shell
if [[ -n "${MPI_ENV_SOURCED:-}" ]]; then
  return 0
fi

MPI_ENV_ENABLE=${MPI_ENV_ENABLE:-auto}
if [[ "$MPI_ENV_ENABLE" =~ ^(0|false|off)$ ]]; then
  MPI_ENV_SOURCED=1
  return 0
fi

# Skip automatic sourcing when set to auto and no known provider is available
ONEAPI_SET_VARS=${ONEAPI_SET_VARS:-"/opt/intel/oneapi/setvars.sh"}
if [[ "$MPI_ENV_ENABLE" == "auto" && ! -f "$ONEAPI_SET_VARS" ]]; then
  MPI_ENV_SOURCED=1
  return 0
fi

if [[ -f "$ONEAPI_SET_VARS" ]]; then
  echo "[mpi-env] Sourcing Intel oneAPI env: $ONEAPI_SET_VARS"
  # shellcheck disable=SC1090
  set +u
  . "$ONEAPI_SET_VARS"
  set -u
  export MPIEXEC=${MPIEXEC:-"/opt/intel/oneapi/mpi/latest/bin/mpiexec"}
else
  echo "[mpi-env] Expected MPI setup script not found: $ONEAPI_SET_VARS" >&2
fi

MPI_ENV_SOURCED=1
return 0
