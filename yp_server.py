import json
import time
import requests
import http.server
import socketserver

JSON_PATH = './yp.json'
INTERVAL = 60
PORT = 7144

# yp_serverを起動
class IndexTxtRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/index.txt':
            self.path = '/public/index.txt'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

index_txt_handler = IndexTxtRequestHandler
yp_server = socketserver.TCPServer(("", PORT), index_txt_handler)
yp_server.serve_forever()

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

