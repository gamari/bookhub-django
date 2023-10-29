
- ホスト側で証明書を発行する
- 

## インストール

https://softwarenote.info/p3954/

### Python経由でのインストール

sudo dnf install -y python3 augeas-libs pip

sudo python3 -m venv /opt/certbot/
sudo /opt/certbot/bin/pip install --upgrade pip
sudo /opt/certbot/bin/pip install certbot
sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot

sudo certbot certonly --standalone
- 説明に答える

- 証明書の確認
ls /etc/letsencrypt