from bs4 import BeautifulSoup
from tkinter import *
import requests
import xlsxwriter


def get_kheirZaman():
    workbook = xlsxwriter.Workbook('kheirzaman.xlsx')

    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'name..')
    worksheet.write('B1', 'price')

    payload = {}
    headers = {
        'deviceId': 'l59exvuo9wduzj1nx24',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.kheirzaman.com/en/category/1/12/Groceries',
        'Sec-Fetch-Dest': 'empty',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'content-language': 'en'
    }

    row = 0
    worksheet.write(row, 0, "name")
    worksheet.write(row, 1, "price")
    row += 1
    for category_number in range(1, 24):
        url = "https://www.kheirzaman.com/portals/public/api/products/filter?categoryIds[0]=" + str(category_number) + "&level=1"
        response = requests.request("GET", url, headers=headers, data=payload)
        pages = response.json()['data']['pagination']['totalPages']
        print("Category number : ", category_number)
        print("Number of pages : ", pages)
        for i in range(pages):
            print("page number : ", i)
            url = "https://www.kheirzaman.com/portals/public/api/products/filter?categoryIds[0]=" + str(category_number) + "&level=1&page=" + str(i)
            response = requests.request("GET", url, headers=headers, data=payload)
            products = len(response.json()['data']['products'])
            for j in range(products):
                worksheet.write(row, 0, response.json()['data']['products'][j]['name'])
                worksheet.write(row, 1, response.json()['data']['products'][j]['finalPrice'])
                row += 1
                # print("product: ", response.json()['data']['products'][j]['name'])
                # print("price: ", response.json()['data']['products'][j]['finalPrice'])
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

        pageLimit = soup.find("p", class_="-gy5 -phs")
        page_Limit = int(pageLimit.text.split()[0])
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

    fileList = ["Names", "Prices"]

    workBook = xlsxwriter.Workbook("Jumia.xlsx")
    workSheet = workBook.add_worksheet()

    workSheet.write(0, 0, fileList[0])
    workSheet.write(0, 1, fileList[1])
    row = 2

    for i in range(len(Names)):
        if Names[i] != "":
            workSheet.write(row, 0, Names[i])
            workSheet.write(row, 1, Prices[i])
            row += 1
    workBook.close()


def get_AlfaMarket():
    PageNum = 1

    Names = []
    Prices = []

    while True:

        html_text = requests.get(f"https://www.alfamarketeg.com/sheikhzayed_en/groceries?product_list_mode=grid&p={PageNum}")

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

    fileList = ["Names", "Prices"]

    workBook = xlsxwriter.Workbook("AlfaMarket.xlsx")
    workSheet = workBook.add_worksheet()

    workSheet.write(0, 0, fileList[0])
    workSheet.write(0, 1, fileList[1])
    row = 2

    for i in range(len(Names)):
        if Names[i] != "":
            workSheet.write(row, 0, Names[i])
            workSheet.write(row, 1, Prices[i])
            row += 1
    workBook.close()


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

    fileList = ["Names", "Prices"]

    workBook = xlsxwriter.Workbook("MetroMart.xlsx")
    workSheet = workBook.add_worksheet()

    workSheet.write(0, 0, fileList[0])
    workSheet.write(0, 1, fileList[1])
    row = 2

    for i in range(len(Names)):
        if Names[i] != "":
            workSheet.write(row, 0, Names[i])
            workSheet.write(row, 1, Prices[i])
            row += 1
    workBook.close()


def get_hyper():
    fileList = ["Names", "Prices"]

    workBook = xlsxwriter.Workbook("Hyper.xlsx")
    workSheet = workBook.add_worksheet()

    workSheet.write(0, 0, fileList[0])
    workSheet.write(0, 1, fileList[1])
    row = 2

    file = open('HyperURLs.txt')

    content = file.readlines()

    for i in range(0, 35):

        print("we're at page : " + str(i))

        payload = {}
        headers = {
            'Accept': '/',
            'Content-Type': 'application/json',
            'Cookie': '_ga_VGXB4S2THQ=GS1.1.1657112536.3.1.1657118382.60; _hjAbsoluteSessionInProgress=0; _hjSession_2474687=eyJpZCI6IjMzMWYyNjE0LWU4YTYtNDA1ZC1iY2RhLWU5YWY2NWRkYzFjYSIsImNyZWF0ZWQiOjE2NTcxMTI1NDQxMDYsImluU2FtcGxlIjpmYWxzZX0=; PHPSESSID=4312513000c13eb01e4ac5162123dd48; _hjSessionUser_2474687=eyJpZCI6IjAzNjdhNmQ5LTQzMzMtNTk1MS05MWE2LWM1MzQ5ODU3YWUyNiIsImNyZWF0ZWQiOjE2NTcxMDMyMzcwNDAsImV4aXN0aW5nIjp0cnVlfQ==; _clck=ichuuk|1|f2x|0; _ga=GA1.1.1076591653.1657103233; _gcl_au=1.1.537592782.1657103233; private_content_version=c2287487b6319656dbe3c3e6372fdea8',
            'Content-Language': 'en',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Host': 'mcprod.hyperone.com.eg',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
            'Referer': 'https://www.hyperone.com.eg/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Store': 'default'
        }

        response = requests.request("GET", content[i], headers=headers, data=payload)
        names = []
        prices = []

        pages = response.json()['data']['connection']['pageInfo']['totalPages']

        for j in range(1, pages + 1):
            response = requests.request("GET", content[i].replace('1', str(j), 1), headers=headers, data=payload)
            for k in range(len(response.json()['data']['connection']['nodes'])):
                names.append(response.json()['data']['connection']['nodes'][k]['name'])
                prices.append(response.json()['data']['connection']['nodes'][k]['price_range']['maximum_price']['final_price']['value'])

        for j in range(len(response.json()['data']['connection']['nodes'])):
            workSheet.write(row, 0, names[j])
            workSheet.write(row, 1, prices[j])
            row += 1
        print("Page number : " + str(i) + " switched")

    workBook.close()


screen = Tk()
screen.geometry("500x450")
screen.title('PythonGuides')
screen.config(bg='#223441')
screen.resizable(width=False, height=False)


def newTask():
    choice = lb.get(ANCHOR)
    label = Label(screen, text="please wait", font=('Times', 18), bg='#223441', fg='white')
    label.place(relx=0.38, rely=0.8)
    if choice == 'MetroMart':
        get_MetroMart()
    elif choice == 'kheirZaman':
        get_kheirZaman()
    elif choice == 'Jumia':
        get_Jumia()
    elif choice == 'AlfaMarket':
        get_AlfaMarket()
    elif choice == 'Hyper':
        get_hyper()


lb = Listbox(screen, width=25, height=8, font=('Times', 18), bg='black', fg='white', selectbackground='#a6a6a6')
lb.place(relx=0.2, rely=0.1)
task_list = [
    'MetroMart',
    'kheirZaman',
    'Jumia',
    'AlfaMarket',
    'Hyper',
]

for item in task_list:
    lb.insert(END, item)

addTask_btn = Button(screen, text='View excell', font=('times 14'), bg='#c5f776', pady=10, command=newTask)
addTask_btn.place(relx=0.4, rely=0.63)

screen.mainloop()
