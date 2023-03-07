<div align="center">
  <h1><strong>MobameSync</strong></h1>
<div>

## 説明

このアップリは`colmsg`に触発されています。 
このアップリの目的は坂道グループシリーズのモバメから
メッセージを存在します。 それだけではなく、`Mobamesync`も
テレグラムにメッセージを同期できます。 

## 前提条件

1. python3とpip
```shell script
apt install python3 python-pip
```

2. レポジトリをクロンして
  ```shell script
  git clone https://github.com/hashinami46/MobameSync.git
  ```

3. 必要なものをインストールして
  ```shell script 
  pip install -r requirements.txt
  ```

4. `config.json`にリフレッシュトーケンを追加して
  ```shell script 
  ...
  "nogizaka46": {
      "refresh_token": "<YOUR REFRESH TOKEN HERE>",
      "access_token": "<YOU CAN KEEP IT EMPTY>",
  ...
  ```

5. テレグラムに同期したいなら`config.json`にこのような例を編集しなさい。
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
