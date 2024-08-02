#!/bin/bash

SAVE_DIR=$1
NUM=$2
SHA256_PATH=$3
YEAR=$4
LABEL=$5
SAVE_DIR=${SAVE_DIR}/${YEAR}/${LABEL}
SHA256_PATH=${SHA256_PATH}/${YEAR}_${LABEL}.txt
INPUT=/home/luis/download/latest.csv

echo ${SHA256_PATH}

nohup az -n ${NUM} \
	-k 257682796e89766159c413146465922afb6df9aa8ebca588bad5ce77769e99b2 \
	-t 20 \
	-o ${SAVE_DIR} \
	-i ${INPUT} \
	--sha256 ${SHA256_PATH} \
	> log/download_${YEAR}_${LABEL}.log 2>&1 &
