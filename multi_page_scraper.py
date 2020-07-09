"""
    script finds number of pages on webpage then extracts all climbing shoe names and prices and prints them to csv file.
"""
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

#set vars
PriceLimit = 65 #set price limit
Size = 9 #set your shoe size
ShoeSizes = {'7' : '2753' , '8': '2757' , '9': '2759', '10': '2762', '11': '2765', '12': '3851'}

filename = "climbingshoes.csv"
f = open(filename, "w")
headers = "Name, RRP (£), Price (£), Link \n"
f.write(headers)
#website is filtered for men and unisex
website  = 'https://shop.epictv.co.uk/en/category/climbing-shoes?f%5B0%5D=field_gender%3A497&f%5B1%5D=field_gender%3A496&f%5B2%5D=field_product%253Afield_shoe_size%3A' + ShoeSizes.get(str(Size)) + '&page='


uClient = uReq(website) #opens up url and downloads info
page_html = uClient.read() #saves source code as this var
uClient.close()
page_soup = soup(page_html, "html.parser")
find_pages = page_soup.findAll("li", {"class":"pager-item desktop"})
page_total = len(find_pages) + 1
for page in range(0, page_total):

    my_url = website + str(page)

    uClient = uReq(my_url) #opens up url and downloads info
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    products = page_soup.findAll("div", {"class":"product-item-row clearfix"})


    ##########

    for idx, product in enumerate(products): #idx gives location (from 0)
        _price = product.findAll("span", {"class":"price-value"})
        price = _price[0].text.replace('£','')
        if float(price) < PriceLimit:
            _name = product.findAll("div", {"class":"field-name-title-field"})
            _rrp = product.findAll("div", {"class":"price-strikethrough"})
            name = _name[0].text.strip()
            full_link = 'https://shop.epictv.co.uk' + str(_name[0].a.attrs['href'])
            rrp = _rrp[0].text.strip().replace('£','')

            f = open(filename, "a")
            f.write(name + "," + rrp + "," + price + "," + full_link  + "\n")

    f.close()
