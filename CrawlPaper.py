import rumps
import time
import schedule
import set_wallpaper_functions as wallpaper
import crawl_functions as crawl

# source /Users/jonathanolson/Projects/Environments/crawl_venv/bin/activate


# Create app using the following call to PyInstaller
    # pyinstaller --clean --onefile --noconsole  CrawlPaper.py
# Edit the file CrawlPaper/Contents/Info.plist to inclue the following key-value pair
        # <key>LSBackgroundOnly</key>
        # <string>True</string>
@rumps.timer(2)
def timerFunction(sender):
    print('Timer running')
    sender.updateWallpaper()

class CrawlPaper(rumps.App):
    def __init__(self):
        super(CrawlPaper, self).__init__(type(self).__name__, icon="/Users/jonathanolson/GitHub/crawlpaper/StatusBarButtonImage@2x.png", template=True)
        self.currentWallpaper = None
        self.menu = ["Update Wallpaper", "Download New Wallpapers", 
        "Delete Current Wallpaper", "Delete All Wallpapers",
        "Enable Wallpaper Auto Update", "Disable Wallpaper Auto Update"]
        self.timer = rumps.Timer(self.updateWallpaper, 60)
        self.timer.start()
        rumps.debug_mode(True)

    @rumps.clicked("Update Wallpaper")
    def updateWallpaper(self, _):
        newWallpaper = wallpaper.setRandomWallpaper(self.currentWallpaper)
        # print('old wallpaper:', self.currentWallpaper, 'new wallpaper:', newWallpaper)
        self.currentWallpaper = newWallpaper

    @rumps.clicked("Download New Wallpapers")
    def downloadNewWallpapers(self, _):
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
        self.timer = rumps.Timer(self.updateWallpaper, 60)
        self.timer.start()

    @rumps.clicked("Disable Wallpaper Auto Update")
    def stopTimer(self, _):
        self.timer = self.timer.stop()


if __name__ == "__main__":
    app = CrawlPaper()
    app.run() 