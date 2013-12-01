#!/bin/bash

cat << EOF > /tmp/infiniteburn.sh
#!/bin/bash
while true;
    do openssl speed;
done
EOF

# 32 parallel 100% CPU tasks should hit even the biggest instances
for i in {1..32}
do
	nohup /bin/bash /tmp/infiniteburn.sh &
done
