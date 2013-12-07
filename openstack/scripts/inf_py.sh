#!/bin/bash

cat << EOF > /tmp/infinite.py
if __name__ == "__main__":
    while(True):
        pass
EOF

nohup python /tmp/infinite.py &
