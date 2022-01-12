if [[ $OSTYPE == linux-gnu* ]]
then
	systemctl stop raw
	sleep 1s
	systemctl status raw
fi