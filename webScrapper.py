import requests
import fbprophet
from bs4 import BeautifulSoup

class BillBoardHot100Scrapper:
    url = ""
    classIdentifierDictionary = {}
    rank = []
    artist = []
    song = []
    title = []

    def __init__(self,url,classIdentifierDictionary,header):
        self.url=url
        self.classIdentifierDictionary = classIdentifierDictionary
        self.title=header

    def scrapeWebContent(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")
        soup.prettify()
        divClassIdentifier = self.classIdentifierDictionary["div"]
        divContent = soup.find("div", {"class":divClassIdentifier})
        return divContent

    def getTop100List(self,divContent):
        olClassId=self.classIdentifierDictionary["ol"]
        liClassId=self.classIdentifierDictionary["li"]
        ol = divContent.find("ol",{"class":olClassId})
        li = ol.find_all("li",{"class":liClassId})
        return li

    def iterateList(self,li):
        rankClassId = self.classIdentifierDictionary["rank"]
        songClassId = self.classIdentifierDictionary["song"]
        artistClassId = self.classIdentifierDictionary["artist"]
        for l in li:
            rank = l.find("span",{"class":rankClassId})
            song = l.find("span",{"class":songClassId})
            artist = l.find("span",{"class":artistClassId})
            self.rank.append(rank.text)
            self.artist.append(artist.text)
            self.song.append(song.text)


    def printTopNListItems(self,n=100):
        longest_Name = max(map(len, self.artist[:n]))
        data = [self.title] + list(zip(self.artist[:n], self.song[:n], self.rank[:n]))
        for i, d in enumerate(data):
            line = '|'.join(str(" "+x).ljust(longest_Name+5) for x in d)
            print(line)
            if i > 0:
                print('-' * len(line))
            if i == 0:
                print('~' * len(line))

def main():
    url = 'https://www.billboard.com/charts/hot-100'
    classIdentifierDictionary = {"div" : "chart-list container",
                                  "ol" : "chart-list__elements",
                                  "li" : "chart-list__element",
                                  "rank" : "chart-element__rank__number",
                                  "song" : "chart-element__information__song",
                                  "artist" : "chart-element__information__artist"}
    header=["Artist","Song","Position"]
    scrapper = BillBoardHot100Scrapper(url,classIdentifierDictionary,header)
    divContent = scrapper.scrapeWebContent()
    list = scrapper.getTop100List(divContent)
    scrapper.iterateList(list)
    scrapper.printTopNListItems()
    #scrapper.printTopNListItems(10) # To get top 10 list


if __name__ == '__main__':
    main()
