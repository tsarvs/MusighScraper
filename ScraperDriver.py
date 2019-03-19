import urllib
import requests
from bs4 import BeautifulSoup
import os

def getSoup(url):
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, "html.parser")
    return soup

def getLatestPost():
    homePage = "http://musigh.com/"

    latestPostURL = getSoup(homePage).find("div", id="content").find_all("div", class_="post-title")[0].find("a")['href']

    return latestPostURL


def getMusicInfo(url):
    soup = getSoup(url)

    article = soup.find("article")

    date = article.find("div", class_="post-date").get_text().split()[0]
    title = article.find("h2").get_text()

    message = title + "\n" + url + "\n" + date + "\n"

    for x in article.find("div", class_="post-content").find_all("p"):
        song = x.find("strong")
        if(song != None):
            message += ("\t" + song.get_text() + "\n")

    return message

def getNext(url):
    soup = getSoup(url)

    next = soup.find("div", class_="oldernewer").find("p", class_="older").find("a")

    if next['rel'][0] != "next":
        return next['href']
    else:
        return ""

def consoleIterate():
    blogpost = getLatestPost()

    while (blogpost != ""):
        print(getMusicInfo(blogpost))
        blogpost = getNext(blogpost)

def downloadMusic(url):
    soup = getSoup(url)

    article = soup.find("article")

    articleLinks = article.find("div", class_="post-content").find_all("a")

    i = 0
    for link in articleLinks:
        if (".mp3" in link['href']):
            try:
                doc = requests.get(link['href'])
                linkURL = link['href'].split("/")
            except:
                print("\tERROR: Could not get link URL")

            try:
                fileName = linkURL[len(linkURL) - 1]
            except:
                print("\tWARNING: could not get file name")
                fileName = "song" + str(i) + ".mp3"

            try:
                year = linkURL[len(linkURL) - 3]
            except:
                print("\tWARNING: using 'Other' for year")
                year = "Other"

            dirName = "Music/" + year + "/"
            try:
                # download file
                if (not os.path.exists(dirName+fileName)):
                    f = open(fileName, "wb")
                    f.write(doc.content)
                    f.close()

                    #directorize file
                    try:
                        if not os.path.exists(dirName):
                            os.makedirs(dirName)

                        os.rename(fileName, dirName + fileName)
                        print("\tFile written to directory: " + dirName + fileName)
                    except:
                        print("\tWARNING: duplicate mp3 " + dirName + fileName)
                        try:
                            print("\tRemoving duplicate...")
                            os.remove(fileName)
                        except:
                            print("\tERROR: Could not remove duplicate file")


            except:
                print("\tERROR: Could not save mp3 #" + str(i))

        i+=1

def scrapeMusic():
    blogpost = getLatestPost()

    i = 0
    while (blogpost != ""):

        print("Post "+str(i))
        print(blogpost)

        downloadMusic(blogpost)

        blogpost = getNext(blogpost)
        i+=1

def menu():
    print("1) List Songs")
    print("2) Download MP3s")
    print("3) Exit")

    userin = input("Select an option: ")
    print()

    return userin

def main():
    print("Musigh Scraper v1.2")
    print("By: Tom Sarver\n")

    option = "0"

    while(option != "3"):

        option = menu()

        if (option == "1"):
            consoleIterate()
        elif (option == "2"):
            scrapeMusic()
        elif (option == "3"):
            print("Program Terminated.")

main()
