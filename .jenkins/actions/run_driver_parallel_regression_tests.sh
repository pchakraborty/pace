#!/bin/bash
set -e -x
BACKEND=$1

export TEST_ARGS="-v -s -rsx --backend=${BACKEND} "

export CPPFLAGS="${CPPFLAGS} -Wno-unused-but-set-variable"

if [ ${python_env} == "virtualenv" ]; then
    CONTAINER_CMD="" MPIRUN_ARGS="" DEV=n make driver_savepoint_tests_mpi
else
    DEV=n make driver_savepoint_tests_mpi
fi
