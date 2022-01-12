sudo apt install python3-pip
python3 -m pip install tornado
python3 -m pip install pygments

if [[ $(pwd) != *raw.gm-lang.org ]]
then
	echo "wrong workplace"
	exit 0
fi
root=$(pwd)

cd $root
git clone https://github.com/GiacomoZheng/pygments_gm.git
mkdir src_cache
mkdir raw
cd $root/raw
git clone https://github.com/GiacomoZheng/gm.git

# shebang
cd $root
sudo chmod +x start
sudo chmod +x stop
sudo chmod +x update
sudo chmod +x restart
sudo chmod +x status
sudo chmod +x run

if [[ $OSTYPE == linux-gnu* ]]
then 
	sudo cp $root/raw.service /etc/systemd/system/raw.service
	sudo systemctl daemon-reload
fi

cd $root
./start