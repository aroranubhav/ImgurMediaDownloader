import argparse, os, sys, yaml
import urllib.request
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

clientId = 'dbd5fda652d458f'
clientSecret = '1b71ba35c93ce83f1f94c4c82f27633f87b6c805'

def main(album_id):
    client = ImgurClient(clientId, clientSecret)

    for album in album_id:
        try:
            images = client.get_album_images(album)
        except ImgurClientError as e:
            print('Status Code {}'.format(e.status_code))
            print('Error {}'.format(e.error_message))

        print("Downloading album {} ({!s} images)".format(album, len(images)))

        # Download each image
        for image in images:
            # Turn our link HTTPs
            link = image.link.replace("http://","https://")
            # Get our file name that we'll save to disk
            file_name = link.replace("https://i.imgur.com/","")
            download_path = os.path.join(args.directory, file_name)
            if os.path.isfile(download_path):
                print("File exists for image {}, skipping...".format(file_name))
            else:
                download_media(link, download_path)
    
def download_media(media_url, download_path):
    """
    Download media and save it to file path
    """
    try:
        download = urllib.URLopener()
        download.retrieve(media_url, download_path)
    except urllib.error.URLError as e:
        print("Error downloading image '{}': {}".format(image_url, e))
    except urllib.error.HTTPError as e:
        print("HTTP Error download image '{}': {!s}".format(image_url, e))

def parse_args():
    parser = argparse.ArgumentParser(description='Download an Imgur album/gallery into a folder.')
    parser.add_argument('-c', '--config', type=argparse.FileType('r'), default=os.path.expanduser('~/.config/imgur_downloader/config.yaml'),
            help='config file to load settings from')
    parser.add_argument('-a', '--album', help='album ID to download from Imgur (can be specified multiple times)', required=True, action='append')
    parser.add_argument('-d', '--directory', default=os.path.dirname(os.path.realpath(__file__)), help='directory to save images into')

    return parser.parse_args()

def load_config(config_file):
    print('Loading config file {}'.format(config_file.name))
    try:
        config = yaml.load(config_file, yaml.BaseLoader)
    except yaml.YAMLError as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Error loading YAML {} on line {}'.format(e, exc_tb.tb_lineno))

    return config

if __name__ == '__main__':
    main()
            



#Function to download media
def download(media_url):
  url = media_url

  try:
    request_image = requests.get(url)
    src = request_image.content.decode('utf-8')
    check_type = re.search(r'<meta name="medium" content=[\'"]?([^\'" >]+)', src)
    check_type_f = check_type.group()
    final = re.sub('<meta name="medium" content="', '', check_type_f)

    if final == "image":
      print("\nDownloading the image...")
      extract_image_link = re.search(r'meta property="og:image" content=[\'"]?([^\'" >]+)', src)
      image_link = extract_image_link.group()
      final = re.sub('meta property="og:image" content="', '', image_link)
      _response = requests.get(final).content
      file_size_request = requests.get(final, stream=True)
      file_size = int(file_size_request.headers['Content-Length'])
      block_size = 1024 
      filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
      #t=tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
      with open(filename + '.jpg', 'wb') as f:
        for data in file_size_request.iter_content(block_size):\
          #t.update(len(data))
          f.write(data)
          #t.close()
          print("Image downloaded successfully")

    if final == "video": 
      msg = True

      if msg:
        print("Downloading the video...")
        extract_video_link = re.search(r'meta property="og:video" content=[\'"]?([^\'" >]+)', src)
        video_link = extract_video_link.group()
        final = re.sub('meta property="og:video" content="', '', video_link)
        _response = requests.get(final).content
        file_size_request = requests.get(final, stream=True)
        file_size = int(file_size_request.headers['Content-Length'])
        block_size = 1024 
        filename = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')
        #t=tqdm(total=file_size, unit='B', unit_scale=True, desc=filename, ascii=True)
        with open(filename + '.mp4', 'wb') as f:
          for data in file_size_request.iter_content(block_size):
            #t.update(len(data))
            f.write(data)
            #t.close()
            print("Video downloaded successfully")

            if msg == "no":
              exit()
  except Exception as e:
    print("Error {}".format(e))