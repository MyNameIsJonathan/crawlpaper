from bs4 import BeautifulSoup
from AppKit import NSScreen
import requests
from PIL import Image
import random
import string
import time

# source /Users/jonathanolson/Projects/Environments/crawl_venv/bin/activate

def getScreenDimensions():
    
    """[Ues NSScreen to return current monitor dimensions]
    
    Returns:
        [tuple] -- [a tuple of two ints: screenWidth, screenHeight]
    """

    screenWidth = int(NSScreen.mainScreen().frame().size.width)
    screenHeight = int(NSScreen.mainScreen().frame().size.height)

    # print('Screen Width:', screenWidth)
    # print('Screen Height:', screenHeight)

    return (screenWidth, screenHeight)

def checkImageSize(choice):
    """[Check to make sure the image randomly chosen has a Wallpaper download 
        link that is of high enough resolution for the given monitor]
    
    Arguments:
        choice {[ bs4.element.Tag ]} -- [this is a beautifulsoup4 element tag,
            retrieved from a soup.find_all('div')]
    
    Returns:
        [dict] -- [returned if 'choice' has an image link that has the 
                    required minimum dimensions for the given monitor]
        [boolean] -- [False -- returned if 'choice' does not have req.
                    dimensions]
    """

    screenWidth, screenHeight = getScreenDimensions()
    wallpaperNumber = 0

    image_url = f"https://www.spacetelescope.org{choice.a['href']}"

    # Find the image itself
    image_source = requests.get(image_url).text
    image_soup = BeautifulSoup(image_source, 'lxml')
    imageOptions = image_soup.find_all('span', class_='archive_dl_text')
    # imageOptions = imageOptions.reverse()

    for imageChoice in imageOptions:
        imageSize = imageChoice.text

        dimensions = imageSize.split('x')

        # print(dimensions)

        try:
            choiceWidth = int(dimensions[0])
            choiceHeight = int(dimensions[1])

            wallpaperNumber += 1

            # print('choiceWidth:', choiceWidth)
            # print('choiceHeight:', choiceHeight)
        
            if (choiceWidth >= screenWidth) and (choiceHeight >= screenHeight):
                myDict = {}
                myDict['URL'] = "https://cdn.spacetelescope.org/archives/images/wallpaper" + str(wallpaperNumber) + choice.a['href'][7:-1] + ".jpg"
                myDict['choiceWidth'] = choiceWidth
                myDict['choiceHeight'] = choiceHeight
                # print(f"{choiceWidth, choiceHeight} - OK")
                return myDict

        except ValueError:
            pass

    return False

def resizeImage(url, imageDimensions, desiredDimensions):

    """[]
    
    Arguments:
        url {[ str ]} -- [a string url to the wallpaper image itself]
        imageDimensions {[ tuple ]} -- [tuple of ints (imageWidth, imageHeight)]
        desiredDimensions {[ tuple ]} -- [tuple of ints (desiredWidth, 
                                                        desiredHeight)]

    Returns:
        [ PIL.Image.Image ] -- [img cropped to desired dimensions]
    """


    imageWidth, imageHeight = imageDimensions
    desiredWidth, desiredHeight = desiredDimensions

    widthCrop = (imageWidth - desiredWidth)//2
    heightCrop = (imageHeight - desiredHeight)//2

    img = Image.open(requests.get(url, stream=True).raw)
    img = img.crop(( widthCrop, heightCrop, widthCrop+desiredWidth, heightCrop+desiredHeight ))

    # print('type(img):', type(img))

    return img

def getImageOptions():

    """[Finds all options for wallpapers from Picture of the Week at
        https://www.spacetelescope.org/images'
    
    Returns:
        [ bs4.element.ResultSet ] -- [ returns the BS results from find_all ]
    """


    # Randomy choose a page on the hubble website to find an image
    url = f'https://www.spacetelescope.org/images/potw/page/{random.randint(1, 23)}/'
    # print('URL:', url)

    # Get image download options for this image
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    imageOptions = soup.find_all('div', class_='col-md-3 col-sm-6 col-xs-12')

    # print('type(imageOptions):', type(imageOptions))

    return imageOptions

def downloadImages(N=5):

    """[wrapper function to download N images, crop them, and save them]
    
    Arguments:
        N {[ int ]} -- [Number of images to download, crop, save]
    
    Returns:
        [None] -- [returns nothing]
    """

    print('downloadImages Called')

    screenWidth, screenHeight = getScreenDimensions()

    imagesSaved = 0
    # whileExecutions = 0

    while imagesSaved < N:

        # Sleep for one second to reduce request frequency in looping
        time.sleep(1)

        # print(f'Beginning of imagesSaved < N loop. Execution number {imagesSaved}')

        # Get a group of pictures of the week to choose from
        imageOptions = getImageOptions()

        # Find downloadOption that has width and height big enough
        while True:

            # print(f'Beginning of while True within while imagesSaved < N. Execution number {whileExecutions}')
            # whileExecutions += 1

            # Chooce a random image from the group of pictures of the week; get its URL
            choice = random.choice(imageOptions)
            
            processedChoice = checkImageSize(choice)

            if processedChoice:

                imageURL = processedChoice['URL']
                imageWidth = processedChoice['choiceWidth']
                imageHeight = processedChoice['choiceHeight']

                # Randonly generate a file name for the current image
                fileName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
                fileDirectory = '/Users/jonathanolson/GitHub/crawlpaper/images/'
                filePath = fileDirectory + fileName + '.jpg'

                img = resizeImage(imageURL, (imageWidth, imageHeight),(screenWidth, screenHeight))
                img.save(filePath)
                imagesSaved += 1
                break


