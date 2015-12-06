#!/bin/bash
source /home/ubuntu/.bashrc
ps -aux | grep redis-server | awk '{print $2}' | xargs kill -9
ps -aux | grep celery | awk '{print $2}' | xargs kill -9
ps -aux | grep "python run_m3.py" | awk '{print $2}' | xargs kill -9
