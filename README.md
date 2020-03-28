# cbbot-py

プリコネクラン「まるまる喫茶」で使用しているクラバトBOTです。

スプレッドシートの各項目の書き換えをコマンドで行えます。


## 機能

- 凸管理（凸回数・凸日数）
- スプレッドシートのキャプチャ送信
- クラバト開催期間取得



## コマンド

- 



## 設定

herokuで動かすことを前提としています。

Heroku CLIを予めインストールしておいてください。
<https://devcenter.heroku.com/articles/heroku-cli>


### Add-ons

以下のアドオンを使用しています。
アプリ作成後に追加してください。

- [cloudcube](https://elements.heroku.com/addons/cloudcube)・・・設定したprefixの値を再起動後も保持するために使用


### 環境変数

1. `.env.example`ファイルの内容を編集後、`.env`にリネーム。

2. heroku-config をインストール（初回のみ）

   ```bash
   $ heroku plugins:install heroku-config
   Installing plugin heroku-config... installed v1.5.3
   ```

3. .envファイル内の環境変数をherokuに適用する

   ```bash
   $ heroku config:push -a アプリ名
   Successfully wrote settings to Heroku!
   ```

参考：<https://qiita.com/MosamosaPoodle/items/6e3b64feb22153fd33b8>


### timezone

タイムゾーンをUTCからJSTに変更する必要があります。

```bash
$ heroku config:add TZ=Asia/Tokyo -a アプリ名
Setting TZ and restarting ⬢ cbbot-py... done, v15
TZ: Asia/Tokyo
```

参考：<https://qiita.com/Horie1024/items/85688099707610f70fa6>