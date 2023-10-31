<!-- サンプル -->
<!-- 0 * * * * /usr/bin/docker-compose -f /path/to/your/docker-compose.yml exec -T web python manage.py recommend >> /path/to/logfile.log 2>&1 -->

## cronのインストール

sudo yum install cronie
sudo systemctl start crond
sudo systemctl enable crond

## 自動ツイート

1. /home/ec2-user/bookhub-django に移動する
2. docker compose exec web python manage.py recommend を実行する

crontab -e

* * * * * cd /home/ec2-user/bookhub-django && /usr/local/bin/docker-compose -f /home/ec2-user/bookhub-django/docker-compose.yml exec -T web python manage.py recommend >> /home/ec2-user/cron_log.log 2>&1

0 * * * * cd /home/ec2-user/bookhub-django && /usr/local/bin/docker-compose -f /home/ec2-user/bookhub-django/docker-compose.yml exec -T web python manage.py recommend >> /home/ec2-user/cron_log.log 2>&1

=> 0分に実行される


* * * * * cd /home/ec2-user/bookhub-django && /usr/local/bin/docker-compose exec -T web python manage.py recommend

grep CRON /var/log/syslog

* * * * * cd /home/ec2-user/bookhub-django && /usr/local/bin/docker-compose exec -T web python manage.py recommend >> /path/to/your/logfile.log 2>&1

sudo cat /home/ec2-user/cron_log.log


### 停止
crontab -eから、該当の行を削除する
crontab -r



0 * * * * /home/ec2-user/run_recommend.sh >> /home/ec2-user/cron_log.log 2>&1
* * * * * /home/ec2-user/run_recommend.sh >> /home/ec2-user/cron_log.log 2>&1


「docker-compose exec web python manage.py recommend」このコマンドを、「/home/ec2-user/bookhub-django」上で行いたいだけなので、ファイルを作りたくないんですが、無理ですか？