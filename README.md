<div align="center">
  <h1><strong>MobameSync</strong></h1>
  
  坂道シリーズモバメダウンローダ
  
</div>

![demo](https://github.com/hashinami46/MobameSync/blob/84e7808cc87ec4bebf25d88998ca0e073e6ffd02/demo.gif)
## 説明
このアプリは colmsg に触発されています。
このアプリの目的は、坂道グループシリーズのモバメから
メッセージを取得することです。さらに、MobameSyncは
テレグラムにメッセージを同期することもできます。

## 特徴
* ✅ rootは必要ではありません
* ✅ Python3をサポートするすべての端末で実行できます
* ✅ 全てのメディアが取得できます

## 前提条件

1. Python3とpipがインストールされていること。
  ```shell script
  apt install python3 python-pip python-virtualenv
  ```

2. リポジトリをクローンして、virtualenvを作ること。
  ```shell script
  git clone https://github.com/hashinami46/MobameSync.git
  cd ~/MobameSync
  virtualenv venv
  source venv/bin/activate
  ```

3. 必要なライブラリをインストールすること。
  ```shell script 
  pip install -r requirements.txt
  ```

4. `config.json`にリフレッシュトークンを追加すること。
  ```shell script 
  ...
  "nogizaka46": {
      "refresh_token": "<YOUR REFRESH TOKEN HERE>",
      "access_token": "<you can leave it empty>",
  ...
  ```
    リフレッシュトケンを取得する方法は[こちら](https://home.gamer.com.tw/artwork.php?sn=5594412)へご覧ください。

5. テレグラムに同期したい場合は、config.jsonを以下のように編集してください。
  **その前に**、botを必ず作ってください
  ```shell script
  ...
  "Telegram_Config": {
    "service": true,
    "servicemode": "prod", 
    "botdebugtoken": "<you can leave it empty>", #example : d40f9901-10a1-4652-b2b4-47f7c20ef804
    "botfinaltoken": "<YOUR BOT TOKEN HERE>",
    "ownerid": <YOUR ID>,
    "botdebuggroup": <you can leave it empty>,
    "botfinalgroup": <YOUR GROUP ID HERE>,
    "prefix": "\u3007\u3007"
  }
  ...
  ```
 
  - service (boolean)
    既定値は `true`
    テレグラムサービスをトグルすること。
  - servicemode (string)
    既定値は `prod`
    `prod`とか`debug`
  - botdebugtoken (string)
    `debug`をするとこの欄が選択されます。
  - botfinaltoken (string)
    `prod`をするとこの欄が選択されます。
  - ownerid (integer)
    ここにテレグラムIDを追加すること。
  - botdebuggroup (integer)
    `debug`をするとこの欄が選択されます。
  - botfinalgroup (integer)
    `prod`をするとこの欄が選択されます。
  - prefix (string)
    既定値は`\u3007\u3007`
    あなたの名前とかツイッターにあるような妄想。

## 使い方

**先ずは**データベースを必ず更新してください。
  ```shell script
  python3 mobame.py -s update
  ```
その後、メッセージがダウンロードできます。
  - もし、「池田瑛紗」からのメッセージを取得なら
  ```shell script
  python3 -s dl -g 乃木坂46 -m 池田瑛紗 -d 2022-03-08
  ```
  - 2つ以上もできます
  ```shell script
  python3 -s dl -g 乃木坂46 -m 池田瑛紗 川崎桜 -d 2022-03-08
  ```
  - もし、「2023-03-01」から「2023-03-10」までメッセージを取得したいなら
  ```shell script
  python3 -s dllist -g 乃木坂46 -m 池田瑛紗 -fd 2022-03-01 -td 2022-03-10
  ```
  - 購読を見たいなら
  ```shell script
  python3 -s check -g 乃木坂46
  ```

## テレグラムと同期設定
**先ずは**その前の構成をチェックして、pythonでtelegrambot.pyを実行すること
  ```shell script
  cd ~/telegram
  python3 telegrambot.py
  ```
その後, botfatherでbotのコマンドを設定
  **AVAILABLE COMMAND**
  - start - Botの紹介
  - subsinfo - アクティブ購読情報
  - tentang - botと開発者のこと
  - konfigurasi - (所有者のみ) トグルサービス
  - ceksyncstate - (所有者のみ) 同期ステータス情報
  - startsync - (所有者のみ) 同期をはじめ
  - stopsync - (所有者のみ) 同期を停止
  - updatetoken - (所有者のみ) リフレッシュトケンをアップデート
  - sendpastmessage - (所有者のみ) 新たな購読のメッセージをシェア
  - sendlog - (所有者のみ) logging.logをダウンロード


## ライセンス

このアプリケーションはオープンソースで提供されており、現状のままで提供されています。
作者は、このアプリケーションによって発生したあらゆる損害について責任を負いません。
また、このアプリケーションを使用することによって、利用者が任意のリスクを負うことに同意するものとします。

このアプリケーションは MIT ライセンスで提供されています。

## 注意事項
アプリの利用規約 第8条（禁止事項）に以下の項目があるため注意してください。
- (16) 当社が指定するアクセス方法以外の手段で本サービスにアクセスし、またはアクセスを試みる行為
- (17) 自動化された手段（クローラおよび類似の技術を含む）を用いて本サービスにアクセスし、またはアクセスを試みる行為
  