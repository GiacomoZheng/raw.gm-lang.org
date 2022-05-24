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
if [[ -d pygments_gm ]]
then
	cd pygments_gm
	echo "pygments_gm:"
	git pull --rebase=false
	cd $root
else
	git clone https://github.com/GiacomoZheng/pygments_gm.git
fi

if [[ -d src_cache ]]
then
	rm -rf src_cache
fi
mkdir src_cache

if [[ -d raw ]]
then
	cd $root/raw/gm
	echo "raw:"
	git pull --rebase=false
	cd $root
else
	mkdir raw
	cd $root/raw
	git clone https://github.com/GiacomoZheng/gm.git
fi


if [[ $OSTYPE == linux-gnu* ]]
then 
	# shebang
	cd $root
	sudo chmod +x start
	sudo chmod +x stop
	sudo chmod +x update
	sudo chmod +x restart
	sudo chmod +x status
	sudo chmod +x run

	sudo cp $root/raw.service /etc/systemd/system/raw.service
	sudo systemctl daemon-reload

	./start

else # other systems
	# mac OS --- darwin*

	cd $root
	bash ./run
fi