from .University import University
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import csv
from dateutil.parser import parse

class Aberdeen(University):
    titleArr = []
    hrefArr = []
    authorArr = []
    dateArr = []
    abstractArr = []
    keywordsArr = []

    def __init__(self):
        pass


    def ScrapeForData(self, isRaw, depth, keywords):
        for i in range(len(keywords)):
            for y in range(depth):
                url = 'https://aura.abdn.ac.uk/discover?rpp=20&etal=0&query='+keywords[i]+'&scope=/&group_by=none&page='+str(y)+'&sort_by=score&order=desc'
                page = requests.get(url)

                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    divs = soup.find_all("div", {"class": "row ds-artifact-item"})

                    for x in tqdm(range(len(divs)), ncols=80, ascii=True, desc=keywords[i] + "; Page " + str(1 + y)):
                        href = divs[x].find("a").get("href")
                        pageMaterial = requests.get("https://aura.abdn.ac.uk/" + href)
                        soup = BeautifulSoup(pageMaterial.text, "html.parser")
                        self.titleArr.append(self.GetTitle(soup))
                        self.hrefArr.append("https://aura.abdn.ac.uk/" + href)
                        self.authorArr.append(self.GetAuthors(soup))
                        self.dateArr.append(self.GetDate(soup))
                        self.abstractArr.append(self.GetAbstract(soup))
                        self.keywordsArr.append(keywords[i])
                else:
                    print("Error: " + str(page.status_code))

        if (isRaw):
            self.OutputRaw()
        else:
            self.OutputCSV()


    def OutputCSV(self):
        with open('out/aberdeen.csv', 'w', newline='', encoding='utf-8') as csvFile:
            headerList = ['Title', 'Href', 'Author', 'Date', 'Abstract', 'Keywords', 'University Name']
            writer = csv.DictWriter(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, fieldnames=headerList)
            writer.writeheader()
            for x in range(len(self.titleArr)):
                writer.writerow({'Title': self.titleArr[x], 'Href': self.hrefArr[x], 'Author': self.authorArr[x], 'Date': self.dateArr[x], 'Abstract': self.abstractArr[x], 'Keywords': self.keywordsArr[x], 'University Name': 'University of Aberdeen'})

    def OutputRaw(self):
        print("Title,Href,Author,Date,Abstract,Keyword,University Name")
        for x in range(len(self.arr)):
            print(self.titleArr[x] + ',' + self.hrefArr[x] + ',' + self.authorArr[x] + ',' + self.dateArr[x] + ',' + self.abstractArr[x] + ',' + self.keywordsArr[x] + 'University of Aberdeen')


    def GetTitle(self, soup):
        title = soup.find("h2", {"class": "page-header first-page-header"}).get_text()
        return title


    def GetAuthors(self, soup):
        authorDiv = soup.find("div", {"class": "simple-item-view-authors item-page-field-wrapper table"}).find_all("div")

        for x in range(len(authorDiv)):
            if x == 0:
                output = authorDiv[x].find("a").get_text()
            else:
                output = output + '; ' + authorDiv[x].find("a").get_text()
        return output


    def GetDate(self, soup):
        dateDiv = soup.find("div", {"class": "simple-item-view-date word-break item-page-field-wrapper table"})
        return parse(dateDiv.get_text(), fuzzy=True).strftime("%B %Y")


    def GetAbstract(self, soup):
        doiDiv = soup.find("div", {"class": "simple-item-view-doi item-page-field-wrapper table"})

        if doiDiv == None:
            return "None"

        doiA = doiDiv.find("a").get("href")
        doiPage = requests.get(doiA)
        soupDoi = BeautifulSoup(doiPage.text, "html.parser")

        abstractDiv = soupDoi.find("blockquote", {"class": "abstract mathjax"})

        if abstractDiv == None:
            return "None"

        finalString = abstractDiv.get_text()
        finalString = finalString.replace("\n", " ")
        finalString = finalString.replace(" Abstract:  ", "")

        return finalString