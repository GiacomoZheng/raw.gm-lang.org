echo "TODO test it"

sudo apt install python3-pip
python3 -m pip install tornado
python3 -m pip install pygments

cd /home/giacomo/
git pull https://github.com/GiacomoZheng/raw.gm-lang.org.git

cd /home/giacomo/raw.gm-lang.org
git clone https://github.com/GiacomoZheng/pygments_gm.git

cd /home/giacomo/raw.gm-lang.org/
mkdir src_cache
mkdir raw
cd /home/giacomo/raw.gm-lang.org/raw
git clone https://github.com/GiacomoZheng/gm.git

cp /home/giacomo/raw.gm-lang.org/raw.service /etc/systemd/system/raw.service
systemctl daemon-reload
systemctl start raw
sleep 1s
systemctl status raw