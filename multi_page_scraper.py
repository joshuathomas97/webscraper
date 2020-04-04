#import bs4 not sure if this is needed

"""
    script finds number of pages on webpage then extracts all climbing shoe names and prices and prints them to csv file.
"""
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

#set vars
price_limit = 70
min_size = 8 #minimum shoe size?
page = 1 #what page do you want to start from?


filename = "climbingshoes.csv"
f = open(filename, "w")
headers = "Name, Price, Link \n"
f.write(headers)

website  = 'https://shop.epictv.co.uk/en/sale/outlet/climbing-shoes-outlet'
uClient = uReq(website) #essentially opens up url and downloads info
page_html = uClient.read() #saves source code as this var
uClient.close()
page_soup = soup(page_html, "html.parser")
find_pages = page_soup.findAll("li", {"class":"pager-item desktop"})
page_total = len(find_pages) + 1
while page < page_total:
    my_url = 'https://shop.epictv.co.uk/en/category/climbing-shoes?page=' + str(page)

    uClient = uReq(my_url) #essentially opens up url and downloads info
    page_html = uClient.read()
    uClient.close()

    #now need to parse html as it is currently a big jumble of text

    page_soup = soup(page_html, "html.parser") #telling it how to parse the file, here as an html source file
    products = page_soup.findAll("div", {"class":"product-item-row clearfix"})

    #gets link
    link = products[0].findAll("div", {"class":"field-name-title-field"})
    full_link = 'https://shop.epictv.co.uk' + str(link[0].a.attrs['href'])
    print(link[0].a.attrs['href'])


    ##########
    filename = "climbingshoes.csv"
    f = open(filename, "a")

    for idx, product in enumerate(products): #idx gives location (from 0)
    #    print('count is', idx+1)

        product_name = product.findAll("div", {"class":"field-name-title-field"})
        name = product_name[0].text.strip()
        full_link = 'https://shop.epictv.co.uk' + str(product_name[0].a.attrs['href'])

        product_price = product.findAll("span", {"class":"price-value"})
        price = product_price[0].text.replace('£','')
        x = float(price)
        if x < price_limit:

            uClient = uReq(full_link)
            page2_html = uClient.read()
            page2_soup = soup(page2_html, "html.parser")
            sizes = page2_soup.findAll("div", {"class":"size-link-wrapper"})
            if len(sizes)>0:
                Lsize = re.findall("\d+", sizes[-1].text)
    #            print(Lsize)
                if float(Lsize[0]) > min_size:
                    Fsize = re.findall("\d+", sizes[0].text)
    #                print('First:', Fsize, 'Last:', Lsize)
                    if float(Fsize[0]) > float(Lsize[0]) or float(Lsize[0])>13:
    #                    print(name, 'number', idx+1, 'must be kids shoe')
                        None
                    else:
                        f.write(name + "," + price + "," + full_link  + "\n")





            #sizes come in order so just end the loop if contains +<10



#sizes[20].text
        #print("Shoe: " + name)
        #print("Price: " + price)


#        print (int(price))

    f.close()
    page += 1
