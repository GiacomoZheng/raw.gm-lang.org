if [[ $OSTYPE == linux-gnu* ]]
then
	systemctl start raw
	sleep 1s
	systemctl status raw
fi