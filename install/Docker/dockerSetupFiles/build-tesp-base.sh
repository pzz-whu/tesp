#!/bin/bash

# Copyright (C) 2021-2022 Battelle Memorial Institute
# file: build-tesp-bases.sh


DOCKERFILE="Dockerfile.tesp_base"
TESP_REP="laurmarinovici/tesp"
TESP_TAG=":base"
clear
docker build --no-cache --rm\
             --network=host \
             -f ${DOCKERFILE} \
             -t ${TESP_REP}${TESP_TAG} ./
