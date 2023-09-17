FROM python:3.9

# 環境変数をセット
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Docker内の作業ディレクトリを指定（ここで色々実行される）
WORKDIR /code

# 依存関係をインストール
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# アプリケーションのコードをコピー
COPY . /code/
