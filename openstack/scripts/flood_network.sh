#!/bin/bash

# Adds 1000ms +- 500ms of latency to each packet
sudo tc qdisc add dev eth0 root latency delay 1000ms 500ms

