#!/bin/bash
#
#
#
echo "usage = ./vcscrape.sh vcs &> file1.log & (VC scraper) -or- ./vcscrape.sh sus &> file1.log & (startup capital scraper)"

source ~/.bashrc

  for i in {1..100}; do
    `nohup scrapy crawl $1`
    sleep 60
  done
