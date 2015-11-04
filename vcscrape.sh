#!/bin/bash
#
#
#
echo "usage = ./vcscrape vcs (VC scraper) -or- ./vcscrape sus (startup capital scraper)"
source ~/.bash_profile
for P in {1..1000};
  do scrapy crawl $1;
  sleep 60;
done
