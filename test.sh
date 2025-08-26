#!/bin/bash

url="http://localhost:8000/"

for ((i = 1; i < 100; i++)); do
	curl "$url" >/dev/null 2>&1

done
