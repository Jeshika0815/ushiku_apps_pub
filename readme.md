# シラヤマ作業管理アプリ プロジェクト概要
Copylight T.Saito

**Ver 4.0.1**
## 今バージョンの特徴(修正点)
- 技術面
    - セキュリティ機能の向上(.env, .gitignoreの導入、キーの変更)
- 作業指示票
    - 工番ー枝番の同一の作業員の時間を加算した値を「累積作業時間」とラベリングして表で表示させる
    - ２の数値を作業工数時間割った値を%表示したものを２の下に「達成率」とラベリングして表で表示(100%上限に設定しない設計)

## 前バージョンの修正点
- 作業伝票
    - 作業コードの名称を記載
    - 入力のリスト選択(更新されない)
    - 個人伝票表示のところを個人のみ表示できるようにする
    - 全体伝票を最新順に表示する
    - 全体の作業伝票を集計者・管理者側で修正、削除できるようにする
    - 全体の作業伝票にフィルタ機能を実装
- 一般社員の指示表入力・集計を可能にする
- スクレイピング対策を実施した
- ドキュメントのリンク添付

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