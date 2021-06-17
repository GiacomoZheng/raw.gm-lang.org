echo "TODO test it"

cd /home/giacomo/
git clone https://github.com/GiacomoZheng/raw.gm-lang.org.git

cd /home/giacomo/raw.gm-lang.org
git https://github.com/GiacomoZheng/pygments_gm.git

cd raw.gm-lang.org/
mkdir src_cache
mkdir raw
cd /home/giacomo/raw.gm-lang.org/raw
git https://github.com/GiacomoZheng/gm.git

cp /home/giacomo/raw.gm-lang.org/raw.service /etc/systemd/system/raw.service

systemctl daemon-reload
systemctl start raw
systemctl status raw