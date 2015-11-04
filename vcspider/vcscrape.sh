#!/bin/bash
#
#
#
echo "usage = ./vcscrape.sh vcs &> file1.log & (VC scraper) -or- ./vcscrape.sh sus &> file1.log & (startup capital scraper)"

source ~/.bash_profile

for i in {1..100}; do
  `scrapy crawl $1`
  sleep 60
done
