
## インストール

- Red Hat系
  - sudo yum install git
- Debian系
  - sudo apt-get install git


## SSHの設定

- ssh-keygen -t rsa -b 4096 -C "gamari4552@gmail.com"
  - /home/ec2-user/.ssh/id_rsa
    - ここに作成される
- パスフレーズは空

- cat /home/ec2-user/.ssh/id_rsa.pub
  - 公開鍵を表示

- GitHubに登録する

- git clone ...
