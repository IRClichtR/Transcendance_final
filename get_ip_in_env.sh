#!/bin/bash
get_host_ip() {
	if [[ "$OSTYPE" == "darwin"* ]]; then
        ifconfig en1 | grep 'inet ' | awk '{print $2}'
	else	
		hostname -I | awk '{print $1}'
	fi	
}

ip_address=$(get_host_ip)

if [ ! -f .env ]; then
	echo ".env file not found"
fi 

if grep -q "HOST_IP=" .env; then
	if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/HOST_IP=.*/HOST_IP=$ip_address/" .env
	else
		sed -i "s/HOST_IP=.*/HOST_IP=$ip_address/" .env
	fi	
else
	echo "HOST_IP=$ip_address" >> .env
fi
