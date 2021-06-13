import os
import requests
import json
import re
from datetime import datetime
import urllib.request

class Media:
  def __init__(self, media_name, media_type, media_link):
    self.media_name = media_name
    self.media_type = media_type
    self.media_link = media_link
      

url = 'https://imgur.com/gallery/7ioyxqm'
hot_gallery_url ='https://api.imgur.com/3/gallery/t/hot'
media_path = '/Users/anubhava/Documents/anubhav/CinnamonBear'
internet_check_url = "http://www.google.com/"

def fetchMediaFiles():
  payload={}
  files={}

  headers = {
    'Authorization': 'Client-ID {{client-id}}'
  }

  response = requests.request("GET", hot_gallery_url, headers=headers, data=payload, files=files)

  json_response = response.json()

  with open("response_file.json", "w") as write_file:
      json.dump(response.json(), write_file)

  media_list = set()
  if response.status_code == 200:
    for item in json_response['data']['items']:
      if item['is_album'] == True:
        if len(item['images']) == 1:
          media_name = item['id']
          media_link = item['images'][0]['link']
          media_type = item['images'][0]['type']
          media_list.add(Media(media_name, media_type, media_link))

    for media in media_list:
      download_media(media)  

  else:
    print('Error {}'.format(json_response["data"]["error"]))

# function to download the media
def download_media(media_object):
  media_link = media_object.media_link
  media_type = media_object.media_type

  print(media_link)
  print(media_type)
  

  if (media_type == 'video/mp4'):
    media_name = media_object.media_name + '.mp4'
  else:
    media_name = media_object.media_name + '.png'
  
  saved_media_path = os.path.join(media_path, media_name)
  

  try:
    print("Downloading starts...\n")
    urllib.request.urlretrieve(media_link, saved_media_path)
    print("Download completed..!\n!")
  except Exception as e:
    print(e) 

#Function to check internet connectivity
def connection(internet_check_url, timeout=5):
  try:
        req = requests.get(internet_check_url, timeout=timeout)
        req.raise_for_status()
        print("You're connected to internet\n")
        return True
  except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}.".format(
        e.response.status_code))
  except requests.ConnectionError:
        print("No internet connection available.")
  return False
      
fetchMediaFiles()