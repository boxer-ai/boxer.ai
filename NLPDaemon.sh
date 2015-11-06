#!/bin/bash
#
#
#
echo "usage = ./NLPDaemon.sh vctest4 (VC scraper) -or- ./NLPDaemon.sh crunchbase_startups (startup capital scraper)"

  source ~/.bashrc

  while true; do
    `python NLPDaemon.py $1`
    sleep 60
  done
