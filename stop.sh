if [[ $OSTYPE == linux-gnu* ]]
then
	sudo systemctl stop raw
	sleep 1s
	systemctl status raw
fi