#!/bin/bash

# Restore the packets. Undo flood network and packet drops
sudo tc qdisc del dev eth0 root netem
