# bash backend.py/update.sh

if [[ $(pwd) != *raw.gm-lang.org ]]
then
	echo "wrong workplace"
	exit 0
fi
root=$(pwd)

git pull

cd $root/raw/gm
git pull

cd $root/pygments_gm
git pull


if [[ $OSTYPE == linux-gnu* ]]
then 
	cp $root/raw.service /etc/systemd/system/raw.service
	systemctl daemon-reload
	
	systemctl restart raw
	sleep 1s
	systemctl status raw
fi