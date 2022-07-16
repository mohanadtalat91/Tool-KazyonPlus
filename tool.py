import csv
from typing import List, Any
from bs4 import BeautifulSoup
from tkinter import *
import requests
import xlsxwriter

def get_kheirZaman():
    workbook = xlsxwriter.Workbook('kheirzaman.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'name..')
    worksheet.write('B1', 'price')



    payload={}
    headers = {
      'deviceId': 'l59exvuo9wduzj1nx24',
      'Accept': 'application/json, text/plain, */*',
      'Referer': 'https://www.kheirzaman.com/en/category/1/12/Groceries',
      'Sec-Fetch-Dest': 'empty',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
      'content-language': 'en'
    }



    row=0
    worksheet.write(row, 0, "name")
    worksheet.write(row, 1, "price")
    row+=1
    for category_number in range(1,24):
        url = "https://www.kheirzaman.com/portals/public/api/products/filter?categoryIds[0]="+str(category_number)+"&level=1"
        response = requests.request("GET", url, headers=headers, data=payload)
        pages=response.json()['data']['pagination']['totalPages']
        for i in range(pages):
            url = "https://www.kheirzaman.com/portals/public/api/products/filter?categoryIds[0]="+str(category_number)+"&level=1&page="+str(i)
            response = requests.request("GET", url, headers=headers, data=payload)
            products=len(response.json()['data']['products'])
            for j in range(products):
                worksheet.write(row, 0, response.json()['data']['products'][j]['name'])
                worksheet.write(row, 1, response.json()['data']['products'][j]['finalPrice'])
                row += 1
                print("product: ",response.json()['data']['products'][j]['name'])
                print("price: ",response.json()['data']['products'][j]['finalPrice'])
        print("---------------------------------------------------------------------")

    workbook.close()

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







screen=Tk()
screen.geometry("500x450")
screen.title('PythonGuides')
screen.config(bg='#223441')
screen.resizable(width=False, height=False)
def newTask():
    choice=lb.get(ANCHOR)
    label = Label(screen, text="please wait", font=('Times', 18), bg='#223441', fg='white')
    label.place(relx=0.38, rely=0.8)
    if choice == 'MetroMart':
        get_MetroMart()
    elif choice == 'kheirZaman':
        get_MetroMart()
    elif choice == 'Jumia':
        get_Jumia()
    elif choice == 'AlfaMarket':
        get_kheirZaman()




lb = Listbox(screen,width=25,height=8,font=('Times', 18),bg='black',fg='white',selectbackground='#a6a6a6')
lb.place(relx=0.2,rely=0.1)
task_list = [
    'MetroMart',
    'kheirZaman',
    'Jumia',
    'AlfaMarket',
    ]

for item in task_list:
    lb.insert(END, item)

addTask_btn = Button(screen,text='View excell',font=('times 14'),bg='#c5f776',pady=10,command=newTask)
addTask_btn.place(relx=0.4,rely=0.63)

screen.mainloop()