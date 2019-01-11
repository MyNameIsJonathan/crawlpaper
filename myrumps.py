import rumps
import set_wallpaper_functions as wallpaper
import crawl_functions as crawl

class CrawlPaper(rumps.App):
    def __init__(self):
        super(CrawlPaper, self).__init__(type(self).__name__, icon="/Users/jonathanolson/GitHub/crawlpaper/StatusBarButtonImage@2x.png", template=True)
        rumps.debug_mode(True)

    @rumps.clicked("Update Wallpaper")
    def updateWallpaper(self, _):
        wallpaper.setRandomWallpaper()

    @rumps.clicked("Download New Wallpapers")
    def downloadNewWallpapers(self, _):
        crawl.downloadImages()
    def newWallpapersNotificaton(self, _):
        rumps.notification("5 new wallpapers downloaded")

if __name__ == "__main__":
    CrawlPaper().run()