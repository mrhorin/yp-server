#!/usr/bin/env python
import yaml
import time
import requests
import http.server
import socketserver
import threading
import argparse
import os, os.path
import traceback
import logging

# オプション
parser = argparse.ArgumentParser()
parser.add_argument("--port", "-p", type=int, default=7144 , help="使用するポート番号を指定(default: 7144)")
parser.add_argument("--interval", "-i", type=int, default=60 , help="index.txtの更新間隔を秒単位で指定(default: 60)")
args = parser.parse_args()

YAML_PATH = './yp.yml'
PUBLIC_DIR_PATH = './public/'
LOG_DIR_PATH = './log/'
INTERVAL = args.interval
PORT = args.port

logging.basicConfig(filename=LOG_DIR_PATH + '/error.log', encoding='utf-8', level=logging.ERROR)

class IndexTxtRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/index.txt':
      self.path = PUBLIC_DIR_PATH + '/index.txt'
      return http.server.SimpleHTTPRequestHandler.do_GET(self)

def get_index_txt(url):
  if url[-1] != '/':
    url + '/'
  res = requests.get(url + '/index.txt')
  res.encoding = 'utf-8'
  return res

# YPサーバの起動
def start_yp_server():
  try:
    index_txt_handler = IndexTxtRequestHandler
    yp_server = socketserver.TCPServer(("", PORT), index_txt_handler)
    print("Started YP server at localhost:" + str(PORT))
    yp_server.serve_forever()
  except:
    logging.error(traceback.format_exc())

# index.txtの自動更新を開始
def start_updating_index_txt():
  try:
    print("Started updating index.txt")
    # publicディレクトリを追加
    if not os.path.exists(PUBLIC_DIR_PATH):
      os.mkdir(PUBLIC_DIR_PATH)
    yp_yml = yaml.safe_load(open(YAML_PATH, "r"))
    while True:
      with open(PUBLIC_DIR_PATH + "/index.txt", "w") as f:
        for yp in yp_yml:
          res = get_index_txt(yp['url'])
          if res.status_code == 200: f.write(res.text)
      print("index.txt is updated.")
      time.sleep(INTERVAL)
  except:
    logging.error(traceback.format_exc())

def main():
  t1 = threading.Thread(target=start_yp_server, name='StartYPServer')
  t2 = threading.Thread(target=start_updating_index_txt, name='StartUpdatingIndexTxt')
  t1.start()
  t2.start()

if __name__ == '__main__':
  main()
