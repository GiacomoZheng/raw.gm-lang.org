if [[ $OSTYPE == linux-gnu* ]]
then
	sudo systemctl start raw
	sleep 1s
	systemctl status raw
fi