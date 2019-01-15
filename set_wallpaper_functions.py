from appscript import app, mactypes
import crawl_functions as crawl
import os
import random

def findRandomLocalWallpapers():
    mydir = "/Users/jonathanolson/GitHub/crawlpaper/images"
    myWallpapers = [image for image in os.listdir(mydir) if image.endswith(".jpg")]

    # If no images found, download some
    if len(myWallpapers) < 2:
        crawl.downloadImages()

    myWallpapers = [image for image in os.listdir(mydir) if image.endswith(".jpg")]

    # Choose an image
    myChoice = random.choice(myWallpapers)

    return myChoice

def setWallpaper(imageName):
    app("Finder").desktop_picture.set(mactypes.File(f"/Users/jonathanolson/GitHub/crawlpaper/images/{imageName}"))

def setRandomWallpaper(currentWallpaper=None):
    newWallpaper = findRandomLocalWallpapers()
    while f"/Users/jonathanolson/GitHub/crawlpaper/images/{newWallpaper}" == currentWallpaper:
        newWallpaper = findRandomLocalWallpapers()
    setWallpaper(newWallpaper)
    return "/Users/jonathanolson/GitHub/crawlpaper/images/" + newWallpaper

def removeCurrentWallpaper(wallpaperPath):
    os.remove(wallpaperPath)

def getAllWallpapers():
    
    # Find all current wallpapers
    mydir = "/Users/jonathanolson/GitHub/crawlpaper/images"
    myWallpapers = ["/Users/jonathanolson/GitHub/crawlpaper/images/" + image for image in os.listdir(mydir) if image.endswith(".jpg")]

    return myWallpapers

def removeWallpapers(papersToRemove):

    # Remove each wallpaper
    for image in papersToRemove:
        os.remove(image)

if __name__ == "__main__":
    setRandomWallpaper()