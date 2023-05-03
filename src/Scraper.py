from uni.Manchester import Manchester
from uni.Birmingham import Birmingham
from uni.Surrey import Surrey

class Scraper(object):
    manchester = Manchester()
    birmingham = Birmingham()
    surrey = Surrey()

    def Manchester(self, isRaw, depth):
        self.manchester.ScrapeForData(isRaw, depth, "Maritime")

    def Birmingham(self, isRaw, depth):
        self.birmingham.ScrapeForData(isRaw, depth, "Maritime")

    def Surrey(self, isRaw, depth):
        self.surrey.ScrapeForData(isRaw, depth, "Maritime")