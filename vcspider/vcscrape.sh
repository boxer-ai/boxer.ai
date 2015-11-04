#!/bin/bash
#
#
#
echo "usage = ./vcscrape.sh vcs &> file1.log & (VC scraper) -or- ./vcscrape.sh sus &> file1.log & (startup capital scraper)"

<<<<<<< HEAD
  source ~/.bashrc

  for i in {1..100}; do
    `nohup scrapy crawl $1`
    sleep 60
  done
=======
source ~/.bash_profile

for i in {1..100}; do
  `scrapy crawl $1`
  sleep 60
done
>>>>>>> af68d94688cf028245d405a30dbaa7ee6d9bdf62
