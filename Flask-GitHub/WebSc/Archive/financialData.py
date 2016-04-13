from bs4 import BeautifulSoup
import requests
import time
import json


def search(comp):
    symbol = comp
    url = 'https://uk.finance.yahoo.com/q?s=' + symbol
    webcrawl(url, symbol)


def webcrawl(link, symbol):
    try:
        i = 0
        while i == 0:
            company = symbol
            r = requests.get(link)
            data = r.text
            soup = BeautifulSoup(data, "html.parser")
            # print soup
            p = soup.find("span", attrs={"id": "yfs_l84_" + symbol + ""}).text
            times = time.strftime("%H:%M:%S")
            print(times, p)
            date_of = time.strftime("%d_%m")
            with open("C:/Users/MOYIN/Desktop/Dissertation/Development/WebSc/price" + company + "_"+date_of + ".json",
                       "a") as f:
                di_ct ={times: p}
                json.dump(di_ct,f)
                f.write("\n")
            time.sleep(60)
    except BaseException as e:
        print(str(e))
        time.sleep(5)


