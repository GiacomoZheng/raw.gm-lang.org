apt install python3-pip
python3 -m pip install tornado
python3 -m pip install pygments

if [[ $(pwd) != *raw.gm-lang.org ]]
then
	echo "wrong workplace"
	exit 0
fi
root=$(pwd)

git clone https://github.com/GiacomoZheng/pygments_gm.git
mkdir src_cache
mkdir raw
cd $root/raw
git clone https://github.com/GiacomoZheng/gm.git

if [[ $OSTYPE == linux-gnu* ]]
then 
	cp $root/raw.service /etc/systemd/system/raw.service
	systemctl daemon-reload
	systemctl start raw
	sleep 1s
	systemctl status raw
fi