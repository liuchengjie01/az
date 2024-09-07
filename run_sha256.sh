#!/bin/bash

SAVE_DIR=/data/androzoo/n_malware
NUM=1000
SHA256_PATH=/data/androzoo/n_malware_list/$1
#YEAR=$4
#LABEL=$5
#SHA256_PATH=${SHA256_PATH}/${YEAR}_${LABEL}_malware.txt
INPUT=/home/luis/download/latest.csv

echo ${SHA256_PATH}

nohup az -n ${NUM} \
	-k 257682796e89766159c413146465922afb6df9aa8ebca588bad5ce77769e99b2 \
	-t 20 \
	-o ${SAVE_DIR} \
	-i ${INPUT} \
	--sha256 ${SHA256_PATH} \
	> log/download_$1.log 2>&1 &
