from appscript import app, mactypes
import crawl_functions as crawl
import os
import random
import sys

def localWallpaperCount():

    """[find number of wallpapers in app's images/ folder]
    
    Returns:
        [ int ] -- [number of .jpg files found in images/ folder]
    """

    mydir = getattr(sys, '_MEIPASS','.')+'/'
    myWallpapers = [image for image in os.listdir(mydir) if image.endswith(".jpg")]

    return len(myWallpapers)

def findRandomLocalWallpapers():

    """[ finds a random local wallpaper ]
    
    Returns:
        [ str ] -- [string ending of random image's filename]
    """

    mydir = getattr(sys, '_MEIPASS','.')+'/'
    myWallpapers = [image for image in os.listdir(mydir) if image.endswith(".jpg")]

    # If no images found, download some
    if len(myWallpapers) < 2:
        crawl.downloadImages()

    myWallpapers = [image for image in os.listdir(mydir) if image.endswith(".jpg")]

    # Choose an image
    myChoice = random.choice(myWallpapers)

    return myChoice

def setWallpaper(imageName):

    """[ sets the current monitor's wallpaper to the argument image ]
    """
    mydir = getattr(sys, '_MEIPASS','.')+'/'
    app("Finder").desktop_picture.set(mactypes.File(mydir + imageName))

def setRandomWallpaper(currentWallpaper=None):

    """[ takes argument wallpaper and finds a random, different 
            image. Sets new image as wallpaper ]

    Input:
        [ str ] -- [ wallpaper filename ending ]
    
    Returns:
        [ str ] -- [ new wallpaper full path ]
    """

    # Find new wallpaper image
    newWallpaper = findRandomLocalWallpapers()

    # Make sure new image is different from current wallpaper
    while f"/Users/jonathanolson/GitHub/crawlpaper/images/{newWallpaper}" == currentWallpaper:
        newWallpaper = findRandomLocalWallpapers()

    # Make new, different image current wallpaper
    setWallpaper(newWallpaper)

    # Return complete wallpaper path
    return "/Users/jonathanolson/GitHub/crawlpaper/images/" + newWallpaper

def removeCurrentWallpaper(wallpaperPath):

    """[ deletes current wallpaper file from images ]

    Input:
        [ str ] -- [ complete path to current wallpaper ]

    """

    os.remove(wallpaperPath)

def getAllWallpapers():

    """[ retrieves a list of all images ]
    
    Returns:
        [ list of str ] -- [ returns a list of complete paths for 
                            images in images/ folder ]
    """

    
    # Find all current wallpapers
    mydir = getattr(sys, '_MEIPASS','.')+'/'
    myWallpapers = [mydir + image for image in os.listdir(mydir) if image.endswith(".jpg")]

    return myWallpapers

def removeWallpapers(papersToRemove):

    """[ iterates through images/ folder and deletes each image ]
    """

    # Remove each wallpaper
    for image in papersToRemove:
        os.remove(image)
