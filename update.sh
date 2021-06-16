bash backend.py/update.sh

cd /home/giacomo/raw.gm-lang.org
git pull

cd /home/giacomo/raw.gm-lang.org/raw/gm
git pull

cp /home/giacomo/raw.gm-lang.org/raw.service /etc/systemd/system/raw.service

systemctl daemon-reload
systemctl restart raw
systemctl status raw