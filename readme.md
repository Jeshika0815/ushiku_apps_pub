# シラヤマ作業管理アプリ プロジェクト概要
Copylight T.Saito

# プロジェクト概要
　本プログラムは、一昨年前に行われた株式会社シラヤマとその牛久工場のDX化に向けた企業プロジェクトにて作業内容を記した注文書、作業員が毎日提出する日報を第一段階として電子化したいとのご要望を受け、プロトタイプとして開発したものである。
　ポートフォリオという形で内容を一部変更した上で公開を行なっております。

# 使用技術
- プログラミング言語：Python, Javascript
- 使用フレームワーク：Django
- 使用環境 : miniconda3, visual studio code
- サーバアプリケーション：Nginx, gunicorn
- OCI Compute Instance(Oracle Linux)


# インストーリングスクリプト
ユーザのhomeディレクトリ上に作成(chmod 775 で変更して実行)
```sh
#!/bin/bash

#initialize.sh
# Installing ushiku_apps
if [ ! -d "ushiku_apps" ]; then
    echo "! Installing ushiku_apps "
    git clone -b branchname ~URL~
fi

read -p prompt "initializing >"
if [ $prompt = "S" ] or [ $prompt = "s" ]; then
    echo "! moving noapps and initializing ushiku command"
    mv ~/clones/ushiku_apps/other_noapp ~/
    mv ~/other_noapp/bash/setup.sh ~/
    mv ~/other_noapp/bash/guide_setup.txt ~/
    chmod 775 ~/setup.sh
    set alias ushiku = '~/setup.sh'
    source ~/.bashrc

elif [ $prompt = "V" ] or [ $prompt = "v" ]; then
    echo "! Ver1 Ushiku Initializing"
else
    echo "! Closed."
    exit 0
```

## Installing setup
```sh
#!/bin/bash

# setup_install.sh
if [ ! -d "~/clones" ]; then
    echo "! Your system have not clones directory.."
    mkdir ~/clones
    echo "! Created clones directory"
else
    if [ ! -d "~/clones/ushiku_apps" ]; then
        echo ! installing latest ushiku_apps..
        git clone -b branch_name ~URL~
        echo "! moving noapps and initializing ushiku command"
        mv ~/clones/ushiku_apps/other_noapp ~/
        mv ~/other_noapp/bash/setup.sh ~/
        mv ~/other_noapp/bash/guide_setup.txt ~/
        chmod 775 ~/setup.sh
        echo "alias ushiku = '~/setup.sh'" >> ~/.bashrc 
        source ~/.bashrc
fi