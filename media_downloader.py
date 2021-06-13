import os
import requests
import json

url = 'https://imgur.com/gallery/7ioyxqm'
hot_gallery_url ='https://api.imgur.com/3/gallery/t/hot'

payload={}
files={}

headers = {
  'Authorization': 'Client-ID {{client_id}}'
}

response = requests.request("GET", hot_gallery_url, headers=headers, data=payload, files=files)

json_response = response.json()

with open("response_file.json", "w") as write_file:
    json.dump(response.json(), write_file)

media_list = set()
if response.status_code == 200:
  for item in json_response["data"]["items"]:
    if item['is_album']== False:
      media_list.add(item['link'])
      print(item['link'], end = ' ')
else:
  print('Error {}'.format(json_response["data"]["error"]))








