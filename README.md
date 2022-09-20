# yp-server

- YPでindex.txt取得時にポートチェックを突破したい
- でもマンションや寮生活の糞回線でポート開放ができない…
- VPNも使えない…
- でもAWS、Heroku、VPS等でサーバなら建てれる…

そんなニッチな需要にお答えするスクリプト

## 概要
1. YPサーバ起動（デフォルトはポート7144）
1. ルードディレクトリにあるyp.jsonに登録したYP一覧からindex.txtを取得しpublic/index.txtに保存
1. `http://サーバIPアドレス:7144/index.txt`にアクセスすると、保存したindex.txtを取得できる
1. 一定の間隔（デフォルトでは60秒ごと）でindex.txtを更新する

## ポート開放
以下、CentOS 7で実施した例を示す。
また、サーバのプロバイダ側でパケットフィルタが動いている場合はそちらの設定も忘れないように。
```
firewall-cmd  --permanent --add-port=7144/tcp
firewall-cmd --reload
systemctl restart firewalld
```
