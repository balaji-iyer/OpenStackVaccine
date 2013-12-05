#!/bin/bash


cat << EOF > /tmp/Infinite.java
public class Infinite {
   public static void main(String[] args) {
       while(true);
    }
}
EOF
javac /tmp/Infinite.java
nohup java -cp /tmp Infinite &
