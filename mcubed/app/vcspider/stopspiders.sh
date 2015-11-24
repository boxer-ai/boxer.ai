#!/bin/bash
#
#
#
echo "usage = ./vcscrape.sh vcs &> file1.log & (VC scraper) -or- ./vcscrape.sh sus &> file1.log & (startup capital scraper)"

source ~/.bashrc

`ps aux | grep vcscrape | awk  '{print $2}' | xargs kill -9`
`ps aux | grep scrapy | awk  '{print $2}' | xargs kill -9`
