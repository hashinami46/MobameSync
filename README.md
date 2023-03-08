<div align="center">
  <h1><strong>MobameSync</strong></h1>
</div>

## 説明

このアプリは colmsg に触発されています。
このアプリの目的は、坂道グループシリーズのモバメから
メッセージを取得することです。さらに、MobameSyncは
テレグラムにメッセージを同期することもできます。

## 特徴

:white_check_mark: rootは必要ではありまでん
:white_check_mark: Python3をサポートするすべての端末で実行できます
全てのメディアが取得できます

## 前提条件

1. Python3とpipがインストールされていること。
  ```shell script
  apt install python3 python-pip
  ```

2. リポジトリをクローンすること。
  ```shell script
  git clone https://github.com/hashinami46/MobameSync.git
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

5. テレグラムに同期したい場合は、config.jsonを以下のように編集してください。
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
  ### 説明
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

## :rocket:使い方

**先ずは**データベースを必ず更新してください。
  ```shell script
  python3 mobame.py -s update
  ```
  
その後、メッセージがダウンロードできます。
• もし、「池田瑛紗」からのメッセージを取得なら
  ```shell script
  python3 -s dl -g 乃木坂46 -m 池田瑛紗 -d 2022-03-08
  ```
• 2つ以上もできます
  ```shell script
  python3 -s dl -g 乃木坂46 -m 池田瑛紗 川崎桜 -d 2022-03-08
  ```
• もし「2023-03-01」から「2023-03-10」までメッセージを取得したいなら
  ```shell script
  python3 -s dllist -g 乃木坂46 -m 池田瑛紗 -fd 2022-03-01 -td 2022-03-10
  ```