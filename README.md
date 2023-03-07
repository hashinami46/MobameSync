<div align="center">
  <h1><strong>MobameSync</strong></h1>
</div>

## 説明
このアプリは colmsg に触発されています。
このアプリの目的は、坂道グループシリーズのモバメから
メッセージを取得することです。さらに、MobameSyncは
テレグラムにメッセージを同期することもできます。

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
      "access_token": "<YOU CAN KEEP IT EMPTY>",
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

## 使い方
