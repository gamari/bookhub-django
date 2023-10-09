# 概要

BookHubアプリ。

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


## デプロイ

- .envの準備
- staticファイルの準備
  - `docker compose exec web python manage.py collectstatic`
- docker compose up -d --build
- docker compose exec web python manage.py migrate
- 週間ランキングの作成をする（準備中）