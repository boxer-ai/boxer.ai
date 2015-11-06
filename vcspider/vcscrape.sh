#!/bin/bash
#
#
#
echo "usage = ./vcscrape.sh vcs &> file1.log & (VC scraper) -or- ./vcscrape.sh sus &> file1.log & (startup capital scraper)"

source ~/.bashrc

  while true; do
    `scrapy crawl $1`
    sleep 1
  done
