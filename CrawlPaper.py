import rumps
import time
import schedule
import os
import sys
import set_wallpaper_functions as wallpaper
import crawl_functions as crawl

# Initialization info:

    # source /Users/jonathanolson/Projects/Environments/crawl_venv/bin/activate

    # Create app using the following call to PyInstaller
        # pyinstaller --clean --onefile --noconsole CrawlPaper.spec
    # Edit the file dist/CrawlPaper.app/Contents/Info.plist to inclue the following key-value pair
            # <key>LSBackgroundOnly</key>
            # <string>True</string>

# Specify local path for images
try:
    base_path = getattr(sys, '_MEIPASS','.')+'/'
except Exception:
    base_path = os.path.abspath(".")



# Define the wrapper function for the timer class
@rumps.timer(2)
def timerFunction(sender):
    print('Timer running')
    sender.updateWallpaper()

class CrawlPaper(rumps.App):
    """[A class to define the CrawlPaper App]
    
    Arguments:
        rumps {[empty]} -- [no input required -- simply run app via app.run()]
    """

    def __init__(self):

        # Create subclass of rumps.App
        super(CrawlPaper, self).__init__(type(self).__name__, icon="/Users/jonathanolson/GitHub/crawlpaper/mymenubaricon.png", template=True)
        self.currentWallpaper = None
        self.timer = rumps.Timer(self.updateWallpaper, 60)
        self.timer.start()
        self.menu = ["Update Wallpaper", "Download New Wallpapers", 
        "Delete Current Wallpaper", "Delete All Wallpapers",
        "Enable Wallpaper Auto Update", "Disable Wallpaper Auto Update"]

    @rumps.clicked("Update Wallpaper")
    def updateWallpaper(self, _):

        # Make sure there's enough wallpapers to set new wallpaper
        numberOfLocalWallpapers = wallpaper.localWallpaperCount()
        if numberOfLocalWallpapers < 2: 
            rumps.alert("Not enough local wallpapers found. \
            Downloading new wallpapers now.")

        # Set new wallpaper
        newWallpaper = wallpaper.setRandomWallpaper(self.currentWallpaper)
        self.currentWallpaper = newWallpaper

    @rumps.clicked("Download New Wallpapers")
    def downloadNewWallpapers(self, _):

        # Alert user of new download -- takes ~10 seconds.
        rumps.alert(message='Downloading new wallpapers. Please wait!')
        crawl.downloadImages()

    @rumps.clicked("Delete Current Wallpaper")
    def deleteCurrentWallpaper(self, _):

        # Select current wallpaper
        oldWallpaper = self.currentWallpaper

        # Set new wallpaper
        newWallpaper = wallpaper.setRandomWallpaper(self.currentWallpaper)
        self.currentWallpaper = newWallpaper

        # Remove old wallpaper
        wallpaper.removeCurrentWallpaper(oldWallpaper)

    @rumps.clicked("Delete All Wallpapers")
    def removeAllWallpapers(self, _):

        # Get current list of wallpapers
        papersToRemove = wallpaper.getAllWallpapers() 
        print('Papers to remove:', papersToRemove)

        # Download new wallpapers
        crawl.downloadImages()

        # Delete old wallpapers
        wallpaper.removeWallpapers(papersToRemove)

        # Set new wallpaper
        self.currentWallpaper = wallpaper.setRandomWallpaper(self.currentWallpaper)

    @rumps.clicked("Enable Wallpaper Auto Update")
    def startTimer(self, _):

        # Start a new timer when this button is clicked
        self.timer = rumps.Timer(self.updateWallpaper, 60)
        self.timer.start()

    @rumps.clicked("Disable Wallpaper Auto Update")
    def stopTimer(self, _):

        # Stop the current instance's timer when clicked
        self.timer = self.timer.stop()


if __name__ == "__main__":
    app = CrawlPaper()
    app.run() 