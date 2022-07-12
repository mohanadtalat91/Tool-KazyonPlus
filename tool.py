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


def get_AlfaMarket():
    PageNum = 1

    Names = []
    Prices = []

    while True:

        html_text = requests.get(
            f"https://www.alfamarketeg.com/sheikhzayed_en/groceries?product_list_mode=grid&p={PageNum}")

        html_Content = html_text.content
        soup = BeautifulSoup(html_Content, "html5lib")

        pageLimit = soup.find("div", id="am-page-count")

        page_Limit = int(pageLimit.text.split()[0])
        print(page_Limit)
        print(PageNum)

        if PageNum == page_Limit:
            break
        ItemsNamesProduct = soup.find_all("strong", class_="product name product-item-name")
        ItemsPricesProducts = soup.find_all("li", class_="item product product-item")
        ItemsPrices = []
        ItemsNames = []
        for i in ItemsPricesProducts:
            ItemsPrices.append(i.find("span", class_="price").text)

        for i in ItemsNamesProduct:
            ItemsNames.append(i.a.text.replace("\n", ""))

        for i in range(len(ItemsNames)):
            Names.append(ItemsNames[i])
            Prices.append(ItemsPrices[i])

        PageNum += 1
        print("Page switched !!")

    items = [[]]

    for i in range(len(Names)):
        if Names[i] != "":
            items.append([Names[i], Prices[i]])

    fileList = ["Names", "Prices"]
    print(len(items))
    for i in items:
        print(i)

    with open('AlfaMarket.csv', 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fileList)
        writer.writerows(items)


def get_MetroMart():
    PageNum = 1

    Names = []
    Prices = []
    while True:

        print(PageNum)

        html_text = requests.get(f"https://www.metro-markets.com/categoryl1/Commodities/15?page={PageNum}")

        html_Content = html_text.content
        soup = BeautifulSoup(html_Content, "html5lib")

        pageLimit = soup.find("div", class_="result-holder").div.p.text

        page_Limit = int(pageLimit.split()[0])
        print(page_Limit)

        if PageNum > (page_Limit // 12):
            break
        ItemProduct = soup.find_all("div", class_="product-card card")

        ItemsNames = []
        for i in ItemProduct:
            ItemsNames.append(i.a.h5)

        ItemsPrices = soup.find_all("p", class_="after")

        for i in range(len(ItemsNames)):
            if ItemsNames[i] != "":
                Names.append(ItemsNames[i].text.replace('\n                            ', ''))
                Prices.append(ItemsPrices[i].text)
        PageNum += 1
        print("Page switched !!")

    items: List[List[Any]] = [[]]

    for i in range(len(Names)):
        if Names[i] != "":
            items.append([Names[i], Prices[i]])

    for i in items:
        print(i)

    fileList = ["Names", "Prices"]

    with open('MetroMart.csv', 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fileList)
        writer.writerows(items)


get_MetroMart()

get_AlfaMarket()

get_Jumia()
