from PIL import Image
from PIL import ImageOps
import numpy as np
import math

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

from sklearn.cluster import MiniBatchKMeans
from collections import Counter
import cv2 #for resizing image
import time
import glob


inputImage = "thor7.jpg"
imagesFolder = "images"
kcolors = 50
saveName = "thor7_mosaic.png"



def get_dominant_color(image, k=4, image_processing_size = None):
    """
    takes an image as input
    returns the dominant color of the image as a list
    
    dominant color is found by running k means on the 
    pixels & returning the centroid of the largest cluster

    processing time is sped up by working with a smaller image; 
    this resizing can be done with the image_processing_size param 
    which takes a tuple of image dims as input

    uses kmeans batch to go faster

    >>> get_dominant_color(my_image, k=4, image_processing_size = (25, 25))
    [56.2423442, 34.0834233, 70.1234123]
    """
    #resize image if new dims provided
    if image_processing_size is not None:
        image.resize(image_processing_size)

    #reshape the image to be a list of pixels
    image = np.array(image)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    #cluster and assign labels to the pixels 
    clt = MiniBatchKMeans(n_clusters = k)
    labels = clt.fit_predict(image)

    #count labels to find most popular
    label_counts = Counter(labels)

    #subset out most popular centroid
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

    return list(dominant_color)

def getDominantColor(image, k):
    kColoredImage = image.convert('P', palette=Image.ADAPTIVE, colors=k).convert('RGB')
    colors = kColoredImage.getcolors()
    colors.sort(key=lambda x: -x[0])
    return colors[0][1]




comics = []
# Get the comic books
preImages = glob.glob(imagesFolder + "/*.jpg")

for i in preImages:
    f = open(i, 'rb')
    img = Image.open(f)
    comics.append(img)




#Looping through comic books to get dominant colors
dominantColors = []
for comic in comics:
    #dominantColor = getDominantColor(comic, 3)
    dominantColor = get_dominant_color(comic, 4)
    dominantColors.append(dominantColor)

palette = np.array(dominantColors).flatten()







image = Image.open(inputImage).convert("RGB")
im = np.array(image)
imWidth = im.shape[1]
imHeight = im.shape[0]
print(imHeight)
print(imWidth)


rows = 50

comicHeight = imHeight/rows
comicWidth = comicHeight/1.5

cols = int(math.ceil(imWidth/comicWidth))


# Going through and finding the dominant color of each portion of the input image
newImage = np.empty((rows, cols, 3))
r = 0
s = time.time()
for y in np.linspace(0, imHeight, rows, endpoint=False):
    Y = math.floor(y)
    c = 0
    for x in np.linspace(0, cols*comicWidth, cols, endpoint=False):
        X = math.floor(x)
        box = (X, Y, X + math.floor(comicWidth), Y + math.floor(comicHeight))

        a = time.time()
        tile = image.crop(box)
        b = time.time()
        #print("Crop time:")
        #print((b-a)*10000)

        a = time.time()
        #dominantColor = get_dominant_color(np.array(tile))
        dominantColor = np.array(tile.convert('P', palette=Image.ADAPTIVE, colors=1).convert('RGB'))[0][0]
        b = time.time()
        #print("Dominant Color time:")
        #print((b-a)*10000)

        newImage[r][c][:] = dominantColor
        c+=1
    r+=1
    print(r)
e = time.time()
print(e-s)
img = Image.fromarray(newImage.astype("uint8"), 'RGB')
#img.show()

# Adjusting palates to help convert to comic books
img = img.convert('P', palette=Image.ADAPTIVE, colors=kcolors).convert('RGB')

#now that we have this image that has been quanzied, assign a comic book to it
print(np.array(img).shape)
indexes = []
for pixel in np.reshape(np.array(img), (-1, 3)):
    smallestErr = 1000
    ind = 0
    smallestInd = 0
    for color in dominantColors:
        err = math.sqrt(pow(pixel[0]-color[0], 2) + pow(pixel[1]-color[1], 2) + pow(pixel[2]-color[2], 2))
        if err < smallestErr:
            smallestInd = ind
            smallestErr = err
        ind+=1
    indexes.append(smallestInd)
#img.show()

cWidth = 50
cHeight = 75

mosaic = Image.new("RGB", (cWidth * cols, cHeight * rows))


# Paste the comic book images into the actual iamges
for i in range(len(comics)):
    comics[i] = comics[i].resize((cWidth, cHeight))
for r in range(rows):
    Y = r * cHeight
    for c in range(cols):
        X = c * cWidth
        box = (X, Y, (X + cWidth), (Y + cHeight))
        index = indexes[r*cols + c]
        mosaic.paste(comics[index], box=box)

mosaic.save(saveName, "PNG")
mosaic.show()
