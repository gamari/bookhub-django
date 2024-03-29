# 概要

BookHubアプリ。

[GitHub](https://github.com/gamari/bookhub-django)
[ローカル](http://localhost:8000/)
[検証用サーバー](https://gamari-devs.xyz/)


## プロジェクト説明

- Django + Nginx + sqlite3を利用
- カスタムユーザーを行えるようにしている
- 認証はsimple jwtを採用


## コンテナ

- docker-compose.yml
    - 本番環境
- docker-compose-local.yml
    - 開発環境

## 設定事項

- [ ] .envを用意して下さい。
  - .env-sampleを参考に用意してください。

-  Firebaseの設定
  - [ ] Firebaseのプロジェクトを作成してください
  - [ ] static/js/firebase.jsを作成してください
- [ ]

## デプロイ

- .envの準備
- staticファイルの準備
  - docker compose exec web python manage.py collectstatic
- docker compose up -d --build
- docker compose exec web python manage.py showmigrations
- docker compose exec web python manage.py migrate
- 週間ランキングの作成をする（準備中）

- CICDによるデプロイ

```
git pull
docker compose exec web python manage.py collectstatic
yes
docker compose exec web python manage.py migrate
docker compose restart
```

## オススメツイート
docker compose exec web python manage.py recommend

docker compose exec web python manage.py createselection

docker compose exec web python manage.py createai 

docker compose exec web python manage.py tweet 

## DB操作

- python manage.py shell

```
from your_app_name.models import Follow
Follow.objects.all().delete()
```


## アプリの追加

startappをして次の手順を行う

- appsディレクトリに入れる
- Configにappsを追加
- urls.pyに追加
- INSTALLED_APPSにconfigを指定する

## Command

python manage.py collectstatic


**マイグレーションを戻す**

python manage.py showmigrations
python manage.py migrate [app_name] [migration_name]


## cron

crontab -e

```
0 * * * * cd /home/ec2-user/bookhub-django && docker compose exec -T web python manage.py recommend >> /home/ec2-user/cron_log.log 2>&1

8 12 * * * cd /home/ec2-user/bookhub-django && docker compose exec -T web python manage.py tweet >> /home/ec2-user/cron_log.log 2>&1

48 13 * * * cd /home/ec2-user/bookhub-django && docker compose exec -T web python manage.py tweet >> /home/ec2-user/cron_log.log 2>&1

12 15 * * * cd /home/ec2-user/bookhub-django && docker compose exec -T web python manage.py tweet >> /home/ec2-user/cron_log.log 2>&1

1 19 * * * cd /home/ec2-user/bookhub-django && docker compose exec -T web python manage.py tweet >> /home/ec2-user/cron_log.log 2>&1

33 22 * * * cd /home/ec2-user/bookhub-django && docker compose exec -T web python manage.py tweet >> /home/ec2-user/cron_log.log 2>&1

25 16 * * * cd /home/ec2-user/bookhub-django && docker compose exec -T web python manage.py createselection >> /home/ec2-user/cron_log.log 2>&1

15 18 * * * cd /home/ec2-user/bookhub-django && docker compose exec -T web python manage.py createselection >> /home/ec2-user/cron_log.log 2>&1
```


