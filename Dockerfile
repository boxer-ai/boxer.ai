FROM ubuntu:14.04
MAINTAINER John Montroy  <jmontroy90@gmail.com>

RUN mkdir /srv/m3 && \
	cd /srv/m3

RUN git clone https://github.com/aviyashchin/boxer.ai-semantic-matchmaking-with-cortical.io-NLP.git