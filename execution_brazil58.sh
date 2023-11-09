#!/usr/bin/bash

source ./env/bin/activate
for i in {1..10}; do
  echo "Test $i"
  echo "Exploration"
  python3 main.py -d datasets/brazil58.xml -e 100
  for _ in {1..5}; do
      echo "Exploitation"
      python3 main.py -d datasets/brazil58.xml -e 10 -ex
  done
  mv reports reports.bak$i
done
