#import bs4 not sure if this is needed

"""
    script finds number of pages on webpage then extracts all climbing shoe names and prices and prints them to csv file.
"""
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

filename = "climbingshoes.csv"
f = open(filename, "w")
headers = "Name, Price \n"
f.write(headers)

website  = 'https://shop.epictv.co.uk/en/category/climbing-shoes'
uClient = uReq(website) #essentially opens up url and downloads info
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
find_pages = page_soup.findAll("li", {"class":"pager-item desktop"})
page_count = len(find_pages) + 1
page = 0
while page < page_count:
    my_url = 'https://shop.epictv.co.uk/en/category/climbing-shoes?page=' + str(page)

    uClient = uReq(my_url) #essentially opens up url and downloads info
    page_html = uClient.read()
    uClient.close()

    #now need to parse html as it is currently a big jumble of text

    page_soup = soup(page_html, "html.parser") #telling it how to parse the file, here as an html source file
    products = page_soup.findAll("div", {"class":"product-item-row clearfix"})
    #products = products[0]

    filename = "climbingshoes.csv"
    f = open(filename, "a")

    for product in products:

        product_name = product.findAll("div", {"class":"field-name-title-field"})
        name = product_name[0].text.strip()

        product_price = product.findAll("span", {"class":"price-value"})
        price = product_price[0].text

        #print("Shoe: " + name)
        #print("Price: " + price)
        f.write(name + "," + price + "\n")

    f.close()
    page += 1
