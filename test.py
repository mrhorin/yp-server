import json
import time
import requests

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

print('Runing YP server...')

while True:
  index_txt_list = []
  for i in yp_json:
    res = get_index_txt(i['url'])
    if res.status_code == 200:
      index_txt_list.append(res.text)
  print(index_txt_list)
  time.sleep(INTERVAL)
