#!/bin/bash
source /home/ubuntu/.bashrc
nohup redis-server &
nohup celery worker -A app.celery --loglevel=INFO &> celery.log &
nohup python run_m3.py &> m3.log &
