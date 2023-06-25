# cbbot-py

プリコネクラン「まるまる喫茶」で使用しているクラバトBOTです。

スプレッドシートの各項目の書き換えをコマンドで行えます。


## 機能

- メンバー入退室の通知
- 凸管理（凸回数・凸日数）
  - ユーザー登録・管理機能
  - 日別凸回数記録
  - 凸未報告・凸報告済ロールの自動付け替え
  - 凸管理シートのキャプチャ送信
  - 開催終了時に凸管理シート自動クリア
- クランバトル開催期間取得・表示
- クランバトル開催・日付変更通知


## コマンド

Prefixは`!`として説明します。適宜読み替えてください

※のついたコマンドは`BOT_COMMAND_CHANNEL`のチャンネルでのみ実行できます

★のついたコマンドは`BOT_MANAGER_ROLE`ロールを持つユーザー限定です。

### Link

クリックでジャンプします

- [cbbot-py](#cbbot-py)
  - [機能](#機能)
  - [コマンド](#コマンド)
    - [Link](#link)
      - [Prefix関係](#prefix関係)
      - [テスト関係](#テスト関係)
      - [凸管理関係](#凸管理関係)

#### Prefix関係

- `!prefix`
  - 現在のPrefixを確認する。  
    現在のPrefixの影響を受けない。

- `set_prefix` ★
  
  - Prefixを変更する  
    スペースを含む場合は""で囲む
  - 例
    - `set_prefix !`
    - `set_prefix hoge`

#### テスト関係

- `!help`
  - ヘルプを表示する
- `!test`
  - コマンドテスト用  
    BOTが`テスト`と発言します
- `!hello`
  - メンションテスト用  
    BOTが`Hello!`とメンションを送ります。
- `!embtest`
  - 埋め込みメッセージ（embed）表示テスト用  
    このBOTは埋め込みメッセージを多用しているため、リンクプレビューを有効にする必要があります。  
    「ユーザー設定＞テキスト・画像＞リンクプレビュー（チャットで投稿されたリンクのサイト情報を表示する）」を有効にしてください。

#### 凸管理関係

- ※`!regist`
  - 凸管理シートにユーザーを登録する。
  - 例
    - 自分を登録：`!regist`
    - ユーザー指定 ★：`!regist -u ユーザー名`
- ※`!delete`
  - 凸管理シートからユーザーを削除する。
  - 例
    - 自分を削除：`!delete me`
    - ユーザー指定 ★：`!delete -u ユーザー名`
- ※凸絵文字
  - 凸登録する。  
    あらかじめサーバー絵文字を作成しておく必要があります。
  - 例
    - 1凸：`:attack1:`
    - 2凸：`:attack2:`
    - 3凸：`:attack3:`
- ※`!attack`
  - 凸登録する。  
    凸回数に0を指定すると凸登録を削除します。
  - 例
    - 自分を登録：`!attack 凸回数
    - ユーザー指定 ★：`!attack -u ユーザー名 凸回数`
- `!status`
  - クランバトル開催情報を表示する。
    <https://redive.estertion.win>から情報を取得しています。
- `!reset_attackrole` ★
  - 全員の凸登録ロールをリセットする。
- `!clear_attackrole` ★
  - 全員の凸登録ロールを削除する。
- `!clear_sheet` ★
  - 凸管理シートの凸登録部分とメモ欄1をクリアする。
- `!capture`
  - スプレッドシートのキャプチャ画像を送信する


<!-- 
## 設定

herokuで動かすことを前提としています。

Heroku CLIを予めインストールしておいてください。
<https://devcenter.heroku.com/articles/heroku-cli>


### Add-ons

以下のアドオンを使用しています。  
アプリ作成後に追加してください。

- [cloudcube](https://elements.heroku.com/addons/cloudcube)・・・設定したprefixの値を再起動後も保持するために使用

### Buildpack

以下のビルドパックが必要です。  
アプリ作成後に追加してください。

- heroku-buildpack-python <https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-python>
- heroku-buildpack-apt <https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-apt> -->
<!-- 
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

参考：<https://qiita.com/MosamosaPoodle/items/6e3b64feb22153fd33b8> -->

<!-- 
### timezone

タイムゾーンをUTCからJSTに変更する必要があります。

```bash
$ heroku config:add TZ=Asia/Tokyo -a アプリ名
Setting TZ and restarting ⬢ cbbot-py... done, v15
TZ: Asia/Tokyo
```

参考：<https://qiita.com/Horie1024/items/85688099707610f70fa6> -->
