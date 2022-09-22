#!/usr/bin/env python

import yaml
import time
import requests
import http.server
import socketserver
import threading
import argparse

# オプション
parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p", type=int, default=7144 , help="使用するポート番号を指定(default: 7144)")
parser.add_argument("--interval", "-i", type=int, default=60 , help="index.txtの更新間隔を秒単位で指定(default: 60)")
args = parser.parse_args()

YAML_PATH = './yp.yml'
INTERVAL = args.interval
PORT = args.port

class IndexTxtRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/index.txt':
      self.path = '/public/index.txt'
      return http.server.SimpleHTTPRequestHandler.do_GET(self)

def get_index_txt(url):
  if url[-1] != '/':
    url + '/'
  res = requests.get(url + '/index.txt')
  res.encoding = 'utf-8'
  return res

# YPサーバの起動
def start_yp_server():
  index_txt_handler = IndexTxtRequestHandler
  yp_server = socketserver.TCPServer(("", PORT), index_txt_handler)
  print("Started YP server at localhost:" + str(PORT))
  yp_server.serve_forever()

# index.txtの自動更新を開始
def start_updating_index_txt():
  print("Started updating index.txt")
  yp_yml = yaml.safe_load(open(YAML_PATH, "r"))
  while True:
    with open("./public/index.txt", "w") as file:
      for yp in yp_yml:
        res = get_index_txt(yp['url'])
        if res.status_code == 200:
          file.write(res.text)
    print("index.txt is updated.")
    time.sleep(INTERVAL)

def main():
  t1 = threading.Thread(target=start_yp_server)
  t2 = threading.Thread(target=start_updating_index_txt)
  t1.start()
  t2.start()

if __name__ == '__main__':
  main()
