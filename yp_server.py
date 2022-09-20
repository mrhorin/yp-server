import json
import time
import requests
import http.server
import socketserver

JSON_PATH = './yp.json'
INTERVAL = 60
PORT = 8080

# URLからindex.txtを取得
def get_index_txt(url):
  if url[-1] != '/':
    url + '/'
  return requests.get(url + '/index.txt')

# yp.jsonを開く
yp_json = json.load(open(JSON_PATH, 'r'))
index_txt_list = []

# チャンネルリストの自動更新
while True:
  # index.txtに書き込み
  with open("./public/index.txt", "w") as f:
   for i in yp_json:
    res = get_index_txt(i['url'])
    if res.status_code == 200:
      f.write(res.text)
  print("index.txt is updated.")
  time.sleep(INTERVAL)

# httpサーバー起動
# Handler = http.server.SimpleHTTPRequestHandler
# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#  print("serving at port", PORT)
#  httpd.serve_forever()


