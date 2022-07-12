import csv
from typing import List, Any

from bs4 import BeautifulSoup
import requests


def get_Jumia():
    PageNum = 1

    Names = []
    Prices = []

    while True:

        html_text = requests.get(f"https://www.jumia.com.eg/groceries/?tag=FDYJE&page={PageNum}#catalog-listing")

        html_Content = html_text.content
        soup = BeautifulSoup(html_Content, "html5lib")

        pageLimit = soup.find("p", class_="-gy5 -phs").text
        page_Limit = int(pageLimit.split()[0])
        print(page_Limit)
        print(PageNum)
        if PageNum > (page_Limit // 48):
            break
        ItemsNames = soup.find_all("h3", class_="name")
        ItemsPrices = soup.find_all("div", class_="prc")

        for i in range(len(ItemsNames)):
            Names.append(ItemsNames[i].text)
            Prices.append(ItemsPrices[i].text)
        PageNum += 1
        print("Page switched !!")

    items = [[]]

    for i in range(len(Names)):
        if Names[i] != "":
            items.append([Names[i], Prices[i]])

    fileList = ["Names", "Prices"]

    with open('Jumia.csv', 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fileList)
        writer.writerows(items)


get_Jumia()
