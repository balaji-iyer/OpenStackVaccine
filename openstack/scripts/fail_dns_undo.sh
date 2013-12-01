#!/bin/bash

# Delete  all traffic rule set in fail_dns.sh on port 53
sudo iptables -D INPUT -p tcp -m tcp --dport 53 -j DROP
sudo iptables -D INPUT -p udp -m udp --dport 53 -j DROP
