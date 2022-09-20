import json
import time
import requests
import http.server
import socketserver
import threading
import argparse

parser = argparse.ArgumentParser()

# ポート番号
parser.add_argument("--port", "-p",type=int, default=7144 , help="使用するポート番号を指定(default: 7144)")
# 更新間隔
parser.add_argument("--interval", "-i", type=int, default=60 , help="index.txtの更新間隔を秒単位で指定(default: 60)")

args = parser.parse_args()

JSON_PATH = './yp.json'
INTERVAL = args.interval
PORT = args.port

# yp_serverを起動
class IndexTxtRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/index.txt':
            self.path = '/public/index.txt'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# URLからindex.txtを取得
def get_index_txt(url):
  if url[-1] != '/':
    url + '/'
  return requests.get(url + '/index.txt')

# YPサーバの起動
def start_yp_server():
  index_txt_handler = IndexTxtRequestHandler
  yp_server = socketserver.TCPServer(("", PORT), index_txt_handler)
  print("Started YP server.")
  yp_server.serve_forever()

# index.txtの自動更新を開始
def start_updating_index_txt():
  # yp.jsonを開く
  yp_json = json.load(open(JSON_PATH, 'r'))
  print("Started updating index.txt")
  while True:
    # index.txtに書き込み
    with open("./public/index.txt", "w") as f:
     for i in yp_json:
       res = get_index_txt(i['url'])
       if res.status_code == 200:
         f.write(res.text)
    print("index.txt is updated.")
    time.sleep(INTERVAL)

t1 = threading.Thread(target=start_yp_server)
t2 = threading.Thread(target=start_updating_index_txt)

t1.start()
t2.start()

