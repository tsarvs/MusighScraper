#Musigh Scraper v1.3
#By: Tom Sarver

import urllib
import mechanize
from bs4 import BeautifulSoup
import os

def getBrowser():
    br = mechanize.Browser()
    br.set_handle_robots(False)

    return br

def getSoup(url):
    browser = getBrowser()
    html = browser.open(url).read()

    browser.close()

    soup = BeautifulSoup(html, "html5lib")

    return soup

def getLatestPost():
    url = "http://musigh.com/"

    soup = getSoup(url)
    
    latestPostURL = soup.find("div", id="content").find_all("div", class_="post-title")[0].find("a")['href']

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

def listURL():
    blogpost = getLatestPost()

    i = 0
    while (blogpost != ""):
        print("Post "+ str(i)+": " + blogpost)
        blogpost = getNext(blogpost)
        i+=1

def listSongs():
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
                browser = getBrowser()
                browser.open(link['href']).read()

                doc = browser.open(link['href']).read()
                
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
    print("1) List URLs")
    print("2) List Songs")
    print("3) Download MP3s")
    print("4) Exit")

    userin = input("Select an option: ")
    print()

    return userin

def main():
    option = "0"

    while(option != "4"):

        option = menu()

        if (option == "1"):
            listURL()
        elif (option == "2"):
            listSongs()
        elif (option == "3"):
            scrapeMusic()
        elif (option == "4"):
            print("Program Terminated.")

def testFxn():
    url = "http://www.musigh.com/"

    soup = getSoup(url)

    return soup

main()
#testFxn()