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
        url = "https://www.kheirzaman.com/portals/public/api/products/filter?categoryIds[0]=" + str(
            category_number) + "&level=1"
        response = requests.request("GET", url, headers=headers, data=payload)
        pages = response.json()['data']['pagination']['totalPages']
        print("Category number : ", category_number)
        print("Number of pages : ", pages)
        for i in range(pages):
            print("page number : ", i)
            url = "https://www.kheirzaman.com/portals/public/api/products/filter?categoryIds[0]=" + str(
                category_number) + "&level=1&page=" + str(i)
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
                prices.append(
                    response.json()['data']['connection']['nodes'][k]['price_range']['maximum_price']['final_price'][
                        'value'])

        for j in range(len(response.json()['data']['connection']['nodes'])):
            workSheet.write(row, 0, names[j])
            workSheet.write(row, 1, prices[j])
            row += 1
        print("Page number : " + str(i) + " switched")

    workBook.close()


def get_carrefour():
    fileList = ["Names", "Prices"]

    workBook = xlsxwriter.Workbook("Carrefour.xlsx")
    workSheet = workBook.add_worksheet()

    workSheet.write(0, 0, fileList[0])
    workSheet.write(0, 1, fileList[1])
    row = 2

    categories = ['FEGY1600000',
                  'FEGY1700000',
                  'FEGY1500000',
                  'FEGY1000000',
                  'FEGY6000000',
                  'FEGY1200000',
                  'FEGY1610000',
                  'NFEGY2000000',
                  'NFEGY3000000'
                  ]
    payload = {}
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'www.carrefouregypt.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
        'Referer': 'https://www.carrefouregypt.com/mafegy/en/c/NFEGY2300000',
        'Connection': 'keep-alive',
        'Cookie': 'cart_api=v2; _fbp=fb.1.1658050339677.665574664; _ga=GA1.2.419124956.1658050337; _gid=GA1.2.336108394.1658050337; _ga_BWW6C6N1ZH=GS1.1.1658050337.1.1.1658054899.0; RT="z=1&dm=www.carrefouregypt.com&si=0927b0e8-f0b6-483e-aedc-44c5fc5134ad&ss=l5p4cuta&sl=1c&tt=ae8t&obo=9&rl=1&ld=2pq72&r=3gc5ilad&ul=2pq73&hd=2pq74"; _gat_UA-125827987-3=1; _hjIncludedInPageviewSample=1; _hjIncludedInSessionSample=1; cto_bundle=BXCw018yamE0U1lEZHpHc3ZlbkM0dDhhUkV6ZWc5d2IlMkZneWdZT01NeFdpMHBtSzVTTXRuT0sxWVdtZ1VCWmlldUtvUDVSa3Y2VXJMWFVnTVVPcEU4d2c0ZXdKJTJCNFhaSDhoVWdiMWVtQ2dtdU12TFZ5QXJqOEo5aiUyQmRLYzk2R05ydGRMdA; _hjAbsoluteSessionInProgress=1; _hjSessionUser_2577697=eyJpZCI6IjQxZmRlZTk1LWE3MjItNWZlYS1iMzYzLTUyZTEwNzFlZDQ3YSIsImNyZWF0ZWQiOjE2NTgwNTAzMzkzMzYsImV4aXN0aW5nIjp0cnVlfQ==; _hjSession_2577697=eyJpZCI6IjZmOTExMjZiLWMxYzMtNDZkZi1hMzI5LWM0NjRiMzIxYzAzNCIsImNyZWF0ZWQiOjE2NTgwNTAzMzkzNDMsImluU2FtcGxlIjp0cnVlfQ==; cart_api=v2; bm_sv=815D50E8AD3994AAFE6C390EB9A776CD~YAAQT3tlXyoW0/SBAQAAlY3CCxBM7a8K5W0pNC1wkNy2IjoQiGYKB3j0d3hOWra015WEw+ne5jNCOoJg7U/3AI3pTECfFxj2ai/2tmeH6by/deflxgfiZC11BQoDJHf1gu1MM8TUiRyNIRiQvLp6L/VV2t2LZGmgeRBOXGeTtCs/4IFYyXi9bPypaL2UXHB4ypoC1pBA3rWphzjiALkb2yEEqIKRm1ATIZophD1QYeWatGkqTNY3BzfKyRTxIfxl2qdIMaHl9s1r~1; storeInfo=mafegy|en|EGP; _hjFirstSeen=1; __gads=ID=8a362e5488da6ae8-22cdc6a94bd400cd:T=1658050342:RT=1658054577:S=ALNI_Mb0KuwTIf7ndql8iiHc-TU6aA6MUA; AKA_A2=A; maf-cookie-banner-accepted=true; _sctr=1|1658008800000; __gpi=UID=00000a3f976baacc:T=1658050342:RT=1658050342:S=ALNI_Ma-tLPPLHs5zGo9dJ7l90TgEpPPjQ; _scid=134e15c7-5fbb-4531-a229-47fd071395a3; _gcl_au=1.1.1431116409.1658050337; maf-session-id=ef2753e1-7ecc-48dd-9f3c-dcc7076ba323; mafegy-preferred-delivery-area=Maadi - Cairo; prevAreaCode=Maadi - Cairo; ak_bmsc=13C95799D26658E2E6A2F9A468090C41~000000000000000000000000000000~YAAQHA4VAj8Oo/qBAQAA+xiACxCPW95ksfnJ2pC7BNRYquuD1UFSS58IjzcpsI/wP/Wkvx6fw6R4OZq7UKxXfxRhdDmftWF6ZOXEXzYeT3NehlgFdtwG9pAZc8imEboLnpnMdOazeqz9FPAqmQlx3+EBFTjdhkPc0or5QSUgk9U7PhMUyDgyWleUS7I2J+Eh7JEsb0OUkUd0TAeAUDcOT4RvgSheoApw8mWT3u9qo3WQrgljFWVc3/ZDJ6I73oGkS0uPwjmg/r8z9efdBTQpwFFrY1wrUSzyeTlnp/ms/RlbS7eAExq02hjki+U4dRvTyFQW3RVih/Ztd2bTypvm9h55cvgUA6w15xByh68HdyRQkiDQ6EBIUIgBFycst7Z4triRxkx9kggXUU0CYDbDUZ9XGIVRzjsQyxDIBupa6E9AYYJUJzVZXtUCRj0w1X/+IUMmf62Qa9Y115PDTMNexZL7S5EtIU+G5u72wQJWRfiR8GypZ+o/CFVSWwlWpP2IJohk; cart_api=v2',
        'appid': 'Reactweb',
        'tracestate': '3355720@nr=0-1-3355720-1021845705-4d43cf83960db091----1658054901052',
        'storeid': 'mafegy',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMzNTU3MjAiLCJhcCI6IjEwMjE4NDU3MDUiLCJpZCI6IjRkNDNjZjgzOTYwZGIwOTEiLCJ0ciI6IjQ4MjFmYmRhZjdkZDU0ZWNkNDEzMTkxOWIzNzAxMzE5IiwidGkiOjE2NTgwNTQ5MDEwNTJ9fQ==',
        'userid': 'undefined',
        'credentials': 'include',
        'token': 'undefined',
        'deviceid': '419124956.1658050337',
        'env': 'prod',
        'traceparent': '00-4821fbdaf7dd54ecd4131919b3701319-4d43cf83960db091-01'
    }

    names = []
    prices = []
    totalproducts = 0
    print("the number of : category ", len(categories))
    for i in range(len(categories)):
        print("category : " + str(i))
        url = f"https://www.carrefouregypt.com/api/v7/categories/{categories[i]}?filter=&sortBy=relevance&currentPage=1&pageSize=60&maxPrice=&minPrice=&areaCode=Maadi%20-%20Cairo&lang=en&displayCurr=EGP&latitude=29.967909028696003&longitude=31.266225954206813&nextOffset=0&requireSponsProducts=true&responseWithCatTree=true&depth=3"
        response = requests.request("GET", url, headers=headers, data=payload)
        pages = response.json()['pagination']['totalPages']

        print("number of : pages ", pages)
        for j in range(pages):
            print("page " + str(j))
            url = f"https://www.carrefouregypt.com/api/v7/categories/{categories[i]}?filter=&sortBy=relevance&currentPage=" + str(
                j) + "pageSize=60&maxPrice=&minPrice=&areaCode=Maadi%20-%20Cairo&lang=en&displayCurr=EGP&latitude=29.967909028696003&longitude=31.266225954206813&nextOffset=0&requireSponsProducts=true&responseWithCatTree=true&depth=3"
            response = requests.request("GET", url, headers=headers, data=payload)
            products = response.json()['products']
            totalproducts = totalproducts + len(products)

            for k in range(len(products)):
                names.append(products[k]['name'])
                prices.append(products[k]['price']['price'])

    for m in range(totalproducts):
        print(names[m], prices[m])
        workSheet.write(row, 0, names[m])
        workSheet.write(row, 1, prices[m])
        row += 1
    workBook.close()


screen = Tk()
screen.geometry("500x450")
screen.title('Tool')
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
    elif choice == 'Carrefour':
        get_carrefour()


lb = Listbox(screen, width=25, height=8, font=('Times', 18), bg='black', fg='white', selectbackground='#a6a6a6')
lb.place(relx=0.2, rely=0.1)
task_list = [
    'MetroMart',
    'kheirZaman',
    'Jumia',
    'AlfaMarket',
    'Hyper',
    'Carrefour'
]

for item in task_list:
    lb.insert(END, item)

addTask_btn = Button(screen, text='View excell', font=('times 14'), bg='#c5f776', pady=10, command=newTask)
addTask_btn.place(relx=0.4, rely=0.63)

screen.mainloop()
