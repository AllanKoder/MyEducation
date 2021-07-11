from bs4 import BeautifulSoup
import requests
import csv

AllTopics = []
AllDescriptions = []
MainFocus = []
amountPerSection = []

source = requests.get('https://www.jvis.com/uguide/majordesc.htm').text
soup = BeautifulSoup(source, 'lxml')

article = soup.find(id='contentRow1ColumnMain')
majors = article.find('ol')

descriptions = article.find("div","text")
descriptions.find('ol').decompose()
descriptions.find('p').decompose()

for description in descriptions.findAll('p'):
    addon = description.text.lower().replace('major', '').replace('u.s.', 'US').replace(' this ', '')\
        .replace('[', '').replace(']', '').replace(' the ', ' ')\
        .replace(' a ', ' ').replace(' an ', ' ').replace(' or ', ' ').replace(' are ', ' ').replace(' to ', ' ')\
        .replace(' on ', ' ').replace(' and ', ' ').replace(' of ', ' ')\
        .replace(' from ', ' ').replace(' with ', ' ').replace(' such ', ' ').replace(' may ', ' ')\
        .replace(' as ', ' ').replace(' for ', ' ').replace(' in ', ' ').replace(' go ', ' ')\
        .replace(' such ', ' ').replace(' have ', ' ').replace(' had ', ' ')\
        .replace(' that ', ' ').replace(' who ', ' ').replace(' can ', ' ')\
        .replace(' be ', ' ').replace('s ', ' ').replace(' do ', ' ').replace(' is ', ' ')\
        .replace(',', '').replace(';', '').replace(':', '').split('.')
    MainFocus.append(addon[-1].lower().replace('/',","))
    addon.pop(-1)
    AllDescriptions.append(addon)
    amountPerSection.append(len(addon))

soup = BeautifulSoup(source, 'lxml')
article = soup.find(id='contentRow1ColumnMain')
majors = article.find('ol')
i2 = 0
for major in majors.findAll('li'):
    AllTopics.append(major.text.lower())
    i2 += 1
csv_file = open("UniData.csv", 'w')
csv_writer = csv.writer(csv_file, lineterminator='\n')
csv_writer.writerow(["Uni", "Description","Topic"])
for i in range(len(AllTopics)):
    topic = AllTopics[i].replace(" ","-")
    for thing in AllDescriptions[i]:
        csv_writer.writerow([AllTopics[i],thing,MainFocus[i].split(",")[0]])
csv_writer.writerow(["nothing","                                                                  "])

csv_file.close()
