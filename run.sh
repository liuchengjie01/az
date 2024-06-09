#!/bin/bash

SAVE_DIR=$1
NUM=$2
YEAR=$3
DATE=${YEAR}-01-01:${YEAR}-12-31
INPUT=/home/luis/download/latest.csv

echo ${DATE}
echo ${INPUT}

nohup az -n ${NUM} \
	-k 257682796e89766159c413146465922afb6df9aa8ebca588bad5ce77769e99b2 \
	-t 20 \
	-o ${SAVE_DIR} \
	-vt 0:0 \
	-d ${DATE} \
	-i ${INPUT} \
	> download_${YEAR}.log 2>&1 &
