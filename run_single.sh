#!/bin/bash

SHA256=$1
APIKEY=257682796e89766159c413146465922afb6df9aa8ebca588bad5ce77769e99b2

curl -O -w "http_code: %{http_code}\n" --remote-header-name -G \
	-d apikey=${APIKEY} \
	-d sha256=${SHA256} \
	https://androzoo.uni.lu/api/download
