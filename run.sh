#!/bin/bash
#set +x
#docker stop titiler
#
#set -o allexport
#source .env
#set +o allexport

sudo docker run --name titiler-server --platform linux/amd64 -p 80:80 \
-e HOST=0.0.0.0 \
-e PORT=80 \
-e WEB_CONCURRENCY=1 \
-e CPL_TMPDIR=/tmp \
-e GDAL_CACHEMAX=75% \
-e GDAL_INGESTED_BYTES_AT_OPEN=32768 \
-e GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR \
-e GDAL_HTTP_MERGE_CONSECUTIVE_RANGES=YES \
-e GDAL_HTTP_MULTIPLEX=YES \
-e GDAL_HTTP_VERSION=2 \
-e PYTHONWARNINGS=ignore \
-e VSI_CACHE=TRUE \
-e VSI_CACHE_SIZE=536870912 \
titiler-server:latest
