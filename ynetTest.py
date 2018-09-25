import csv
import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.ynet.co.il/home/0,7340,L-8,00.html')
soup = BeautifulSoup(page.content, 'html.parser')
mainNewData = soup.find_all('a', attrs={'class':'title'})[0] #this is the main report
link = "https://www.ynet.co.il"+mainNewData.get('href') #this is the main report's link
page1 = requests.get(link)
mainSoup = BeautifulSoup(page1.content, 'html.parser')
author = mainSoup.find_all('span', attrs={'class':'art_header_footer_author'})[0].get_text() #this is the main report's author name
moreInfo = "https://www.ynet.co.il/tags/"+author.replace(' ','_') #more reports by this author, if possible

results = soup.find_all('div', attrs={'class':'cell cwide layout1'}) #secondary reports
links = []
pages = []
soups = []
authors = []
names = []
titles = []
for i in range(len(results)):
 curLink = results[i].find('a').get('href')
 if (curLink[0] == '/'):
     curLink = "https://www.ynet.co.il"+curLink
 links[i:] = [curLink]
 pages[i:] = [requests.get(links[i])]
 soups[i:] = [BeautifulSoup(pages[i].content, 'html.parser')]
 titles[i:] = [results[i].get_text()]
 authors[i:] = [soups[i].find_all('span',attrs={'class':'art_header_footer_author'})]
 try: #if there's a tag of this author
    names[i:] = [authors[i][0].find('a').get_text()]
    authors[i:] = [authors[i][0].find('a').get('href')]
 except Exception:
    names[i:] = [authors[i][0].get_text()]
    authors[i:] = ["https://www.ynet.co.il/tags/"+names[0].replace(' ','_')]
    
results1 = soup.find_all('li', attrs={'relative_block'}) #other reports on ynet.co.il
for j in range(len(results1)):
    curLink = results1[j].find('a').get('href')
    if (curLink[0] == '/'):
        curLink = "https://www.ynet.co.il"+curLink
    links[(i+j+1):] = [curLink]
    pages[(i+j+1):] = [requests.get(links[(i+j+1)])]
    titles[(i+j+1):] = [results1[j].get_text()]
    soups[(i+j+1):] = [BeautifulSoup(pages[(i+j+1)].content, 'html.parser')]
    if (len(soups[(i+j+1)].find_all('title',attrs={'lang':'he'}))):
        titles[(i+j+1):] = [soups[(i+j+1)].find_all('title',attrs={'lang':'he'})[0].get_text()]
    authors[(i+j+1):] = [soups[(i+j+1)].find_all('span',attrs={'class':'art_header_footer_author'})]
    if (len(authors[(i+j+1)]) != 0):
        try: #if there's a tag of this author
            names[(i+j+1):] = [authors[(i+j+1)][0].find('a').get_text()]
            authors[(i+j+1):] = [authors[(i+j+1)][0].find('a').get('href')]
        except Exception:
            names[(i+j+1):] = [authors[(i+j+1)][0].get_text()]
            authors[(i+j+1):] = ["https://www.ynet.co.il/tags/"+names[0].replace(' ','_')]
    else: #there isn't available info about this author
        names[(i+j+1):] = ["Unknown"]
        authors[(i+j+1):] = ["Unknown"]

with open('ynetNews.csv', 'w', newline='') as f: #writing info to a CSV file called 'ynetNews.csv'
    thewriter = csv.writer(f)
    thewriter.writerow(['Title', 'Link', 'Author','More Reports By This Author'])
    thewriter.writerow([mainNewData.get_text(),link, author,moreInfo])
    for k in range(len(links)):
        thewriter.writerow([titles[k],links[k],names[k], authors[k]])



