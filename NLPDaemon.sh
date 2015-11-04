#!/bin/bash
#
#
#
echo "usage = ./NLPDaemon.sh vctest4 (VC scraper) -or- ./NLPDaemon.sh crunchbase_startups (startup capital scraper)"

  source ~/.bashrc

  for i in {1..100}; do
    `nohup python NLPDaemon.py $1`
    sleep 60
  done
