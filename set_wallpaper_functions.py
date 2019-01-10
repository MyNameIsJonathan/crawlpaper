from appscript import app, mactypes
import os
import random

def findRandomLocalWallpapers():
    mydir = "/Users/jonathanolson/GitHub/crawlpaper/images"
    myWallpapers = [image for image in os.listdir(mydir) if image.endswith(".jpg")]
    myChoice = random.choice(myWallpapers)
    return myChoice

def setWallpaper(imageName):
    app("Finder").desktop_picture.set(mactypes.File(f"/Users/jonathanolson/GitHub/crawlpaper/images/{imageName}"))

def setRandomWallpaper():
    newWallpaper = findRandomLocalWallpapers()
    setWallpaper(newWallpaper)

if __name__ == "__main__":
    setRandomWallpaper()