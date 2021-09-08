##THIS IS THE SOURCE CODE

import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import csv
import os

conn = sqlite3.connect("firms3.db")
cur=conn.cursor()
URL = "https://clutch.co/sitemap/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results=soup.find(id="development")
ref=list()
firm_elements = results.find_all("a",class_="sitemap-data__wrap-link")
i=0
ref2=list()
for c in results.find_all('a',href=True):
    ref.append(c['href'])
for i in range(len(ref)):
    if i%2==0:
        ref2.append('https://clutch.co/'+ref[i])

s=list()
for a in results.find_all('a'):
    s.append(a.text)
for i in range(len(s)):
    s[i]=s[i].strip()
t=list()
for i in range(len(s)):
    if i%2==0:
        t.append(s[i])

for i in range(len(t)):
    t[i]=t[i].replace("/"," ")
command1="drop table if exists 'Links';"
conn.execute(command1)

command2="create table if not exists 'Links' (Serial integer primary key, Type varchar(30),href varchar(100));"
conn.execute(command2)
conn.commit()


command1="""CREATE TABLE IF NOT EXISTS '{}' (
Company VARCHAR(30),
Website VARCHAR(30),
Rating FLOAT,
Review Count VARCHAR(15),
Hourly Rate VARCHAR(15),
Min Project Size VARCHAR(15),
Employee Size VARCHAR(15),
Location VARCHAR (30));"""
command2="INSERT INTO 'Links' (Type,href) VALUES ('{}','{}');"
command3="""drop table if exists '{}';"""

for i in range(len(t)):
    conn.execute(command3.format(t[i]))
    conn.execute(command1.format(t[i]))
conn.commit()
for i in range(len(t)):
    conn.execute(command2.format(t[i],ref2[i]))
conn.commit()

while True:
    print("""\nEnter your choice
    1	All in Web Developers
    2	All in Software Developers
    3	All in Mobile App Development
    4	All in iPhone App Development
    5	All in Android App Development
    6	All in eCommerce
    7	All in Artificial Intelligence
    8	All in Blockchain
    9	All in AR/VR
    10	All in IoT
    11	All in Ruby on Rails
    12	All in Shopify
    13	All in Wordpress Developers
    14	All in Drupal
    15	All in Magento
    16	All in DOTNET
    17	All in PHP
    18	All in Wearables
    19	All in Software Testing

    Press n to exit""")

    choice=input()
    if choice=='n':
        quit()
    choice=int(choice)
    URL2=ref2[int(choice)-1]
    page2 = requests.get(URL2)
    soup2 = BeautifulSoup(page2.content, "html.parser")
    name=list()
    results2=soup2.find(id="providers")
    firm_elements2 = results2.find_all("h3",class_="company_info")
    for x in firm_elements2:
        name.append(x.text)
    for i in range(len(name)):
        name[i]=name[i].strip()

    for i in range(len(name)):
        name[i]=name[i].replace("'","")

    ####          Company name           ####


    command1="""INSERT INTO '{}' (Company)
                VALUES ('{}');"""

    for n in range(len(name)):
        print(name[n])
        conn.execute(command1.format(t[int(choice)-1],name[n]))
    conn.commit()

    ####      Website        ####

    i=1
    command2="""update '{}' set Website='{}' where "_rowid_"={};"""
    for z in results2.find_all('li',class_='website-link website-link-a'):
        for b in z.find_all('a',class_='website-link__item'):
            conn.execute(command2.format(t[int(choice)-1],b['href'],i))
            print(b['href'])
            i+=1
    conn.commit()

    ####     Rating         #####
    i=1
    command3="""update '{}' set Rating='{}' where "_rowid_"={};"""
    for h in results2.find_all('div',class_='star star-1 star-odd'):
        conn.execute(command3.format(t[int(choice)-1],float(h.text),i))
        print(h.text)
        i+=1
    conn.commit()


    ####      Review          ####
    i=1
    command4="""update '{}' set Review='{}' where "_rowid_"={};"""
    for x in results2.find_all('div',class_='reviews-link'):
        print(x.text.strip())
        conn.execute(command4.format(t[int(choice)-1],str(x.text.strip()),i))
        i+=1
    conn.commit()

    ####   Location,Hourly,Employee      ####
    u=list()
    command5="""update '{}' set (Location,Hourly,Employee) =('{}','{}','{}') where "_rowid_"={};"""
    for x in results2.find_all('div',class_='list-item custom_popover'):
        for y in x.find_all('span'):
            u.append(y.text.splitlines())
    v=list()
    for i in u:
        for j in i:
            v.append(j)
    for i in range(len(v)):
        v[i]=v[i].replace("'","")

    index=1
    i=0
    j=1
    k=2
    while True:
        print(t[int(choice)-1],v[k],v[i],v[j],index)
        conn.execute(command5.format(t[int(choice)-1],v[k],v[i],v[j],int(index)))
        i+=3
        j+=3
        k+=3
        index+=1
        if k>len(v):
            break
    conn.commit()



    ####        MIN    ##########

    command6="""update '{}' set Min='{}' where "_rowid_"={};"""

    index=1
    for x in results2.find_all('div',class_='list-item block_tag custom_popover'):
        for y in x.find_all('span'):
            print(y.text)
            conn.execute(command6.format(t[int(choice)-1],y.text,index))
            index+=1
    conn.commit()
    print ("Exporting data into CSV............")
    cursor = conn.cursor()
    command7="""select * from '{}';"""
    namecsv=t[int(choice)-1]+".csv"
    cursor.execute(command7.format(t[int(choice)-1]))
    with open(namecsv, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

    dirpath = os.getcwd() + namecsv
    print ("Data exported Successfully into {}".format(dirpath))
