USERNAME=$1
REMOTEHOST=$2
PORTNUMBER=$3
while :; do timeout 86395 ssh -gCNq -c blowfish -o ServerAliveInterval=30 $USERNAME@$REMOTEHOST -D$PORTNUMBER -vvv; sleep 5; done
