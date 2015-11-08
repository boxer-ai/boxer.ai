#!/bin/bash

echo "usage = ./NLPDaemon.sh vctest4 (VC scraper) -or- ./NLPDaemon.sh crunchbase_startups (startup capital scraper)"

while true; do
  echo "running python NLPDaemon.py crunchbase_startups"
  python NLPDaemon.py crunchbase_startups
  sleep 60
done
