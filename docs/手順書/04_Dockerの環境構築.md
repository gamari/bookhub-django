# Dockerのインストール

- sudo yum -y install docker
- sudo systemctl start docker
- sudo systemctl enable docker

# Docker composeのインストール

```
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
 mkdir -p $DOCKER_CONFIG/cli-plugins
 curl -SL https://github.com/docker/compose/releases/download/v2.4.1/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
```

chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose


sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

## Userの権限付与

sudo usermod -aG docker $USER

再起動する

次の設定に進む（現状では立ち上がらない）