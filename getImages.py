# importing the requests library 
import requests 
import hashlib
import time
import urllib.request
import config


filename = "thor"
characterid = 1010338

IMAGE_NOT_AVAIL = "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available"


# api-endpoint 
URL = "http://gateway.marvel.com/v1/public/comics"






#ts, hString = get_hash_and_ts_params()
timestamp = str(int(time.time()))
# hash is required as part of request which is md5(timestamp + private + public key)
hash_value = hashlib.md5(timestamp.encode("ascii") + config.privateKey.encode("ascii") + config.publicKey.encode("ascii")).hexdigest()



# defining a params dict for the parameters to be sent to the API 
PARAMS = {'characters':characterid,'ts':timestamp, 'apikey':config.publicKey, 'hash':hash_value, 'limit':str(100), 'offset':str(100)} 
  
# setting headers
headers = {'content-type':'application/json'}

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS, headers=headers) 
  
# extracting data in json format 
data = r.json() 
  

imageUrls = []

# Making the first call to the api to get total and the first 100 images
total = data['data']['total']
for result in data['data']['results']:
    thumbnail = result['thumbnail']
    if (thumbnail and thumbnail['path'] != IMAGE_NOT_AVAIL):
        url = thumbnail['path']
        extension = thumbnail['extension']
        filename = url.split('/')[-1]
        try:
            urllib.request.urlretrieve((url + "/portrait_small."+  extension), "marvel/" + filename + "." + extension)
            imageUrls.append(url + extension)
        except:
            print("Error with request")

# Making another call for each subsequent 100 comic images  
for i in range(100,total, 100):
    print(i)
    #ts, hString = get_hash_and_ts_params()
    timestamp = str(int(time.time()))
    # hash is required as part of request which is md5(timestamp + private + public key)
    hash_value = hashlib.md5(timestamp.encode("ascii") + config.privateKey.encode("ascii") + config.publicKey.encode("ascii")).hexdigest()
    PARAMS = {'characters':characterid,'ts':timestamp, 'apikey':config.publicKey, 'hash':hash_value, 'limit':str(100), 'offset':str(i)} 

    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS, headers=headers)

    data = r.json() 

    # With the data, loop through and pull the images form the marvel website
    total = data['data']['total']
    for result in data['data']['results']:
        thumbnail = result['thumbnail']
        if (thumbnail and thumbnail['path'] != IMAGE_NOT_AVAIL):
            url = thumbnail['path']
            extension = thumbnail['extension']
            filename = url.split('/')[-1]
            try:
                urllib.request.urlretrieve((url + "/portrait_small."+  extension), "marvel/" + filename + "." + extension)
                imageUrls.append(url + extension)
            except:
                print("Error with request")