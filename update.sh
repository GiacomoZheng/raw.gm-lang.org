cd ~/raw.gm-lang.org
git pull

cd ~/raw.gm-lang.org/raw/gm
git pull

sudo cp /home/giacomo/raw.gm-lang.org/raw.service /etc/systemd/system/raw.service

sudo systemctl daemon-reload
sudo systemctl restart raw
sudo systemctl status raw