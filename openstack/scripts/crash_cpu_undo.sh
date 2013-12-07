#!/bin/bash

cat << EOF > /tmp/kill_loop.sh
#!/bin/bash
while true;
do
	pkill -KILL -f openssl
	sleep 1
done
EOF

nohup /bin/bash /tmp/kill_loop.sh &
