import csv
import requests
from bs4 import BeautifulSoup
import loginbot
import time

def get_page(url):
    response = requests.get(url)
    soup = ''
    if not response.ok:
        print('Server responded: ', response.status_code)
        return soup
    else:
        soup = BeautifulSoup(response.text, "html.parser")
    return soup

# def get_desc(src):    
#     soup = get_page(src)    
#     desc = soup.find('div', id='ds_div').find('font').text.strip().replace('\xa0', '')
#     # desc = soup.find('div', class_='ux-layout-section__textual-display ux-layout-section__textual-display--description')
#     return desc

def get_desc(src):    
    soup = get_page(src)
    # desc = soup.find('div', id='ds_div').find('font').find('font').text.strip().replace('\xa0', '')
    desc = soup.find('div', id='ds_div').find('font').text.strip().replace('\xa0', '')
    return desc

def get_detail_data(soup):
    #title
    try:
        # q = soup.find('h1', id='itemTitle').find('span').text
        title = soup.find('h1', class_='x-item-title__mainTitle').find('span').text
        # title = soup.find('h1', id='itemTitle').text.strip().split(q)[1]
        # title = soup.find('h1', class_='x-item-title__mainTitle').text.strip().split(q)[1]
    except:
        title = ''
    # price
    try:        
        # p = soup.find('span', id='price').text.strip()
        p = soup.find('div', class_='x-bin-price__content').find('div', class_='x-price-primary').find('span').get('content')
        # currency, price = p.split(' $')
        # price = price.replace(',', '')
        price = p
    except:
        # currency = ''
        price = '0'
    # img
    try:        
        # img = soup.find('img', id='icImg').get('src')  
        img = soup.find('div', class_='ux-image-carousel-item active image').find('img').get('src')
    except:
        img = ''

    try:        
        shipping = soup.find('div', class_='ux-labels-values__values-content').find('div').find('span', class_="ux-textspans ux-textspans--BOLD").text.strip()
        curr, ship = shipping.split('$')
        ship = ship.replace(',', '')
    except:
        ship = '0'

    try:        
        quantity = soup.find('div', class_='d-quantity__availability').find('span', class_='ux-textspans').text.strip()
        qty = quantity.split(' ')[0]
        # ship = shipping
    except:
        qty = '0'

    try:        
        src = soup.find('iframe', id='desc_ifr').get('src')        
    except:        
        src= ''

    
    total = (float(price)+float(ship))*2
    
    data = {
        'title': title,
        'price': float(price),        
        'shipping': float(ship),
        'total':total,
        'quantity':qty,
        'desc':src,
        'img': img,        
        }    
    return data

def get_all_links(soup):    
    #    link
    try:
        link = soup.find('section', class_='str-items-grid app-layout__block--gutters').find('section', class_='str-items-grid__container').find_all('article', class_='str-item-card str-item-card--undefined ITEM')
        # link = soup.find_all('li', class_='s-item s-item__pl-on-bottom').find('div', class_='s-item__wrapper clearfix').find('div', class_='s-item__info clearfix')
    except:
        link = ''    
    # urls = [item.find('a', class_='s-item__link').get('href') for item in link]    
    urls = [item.find('a', class_='str-item-card__link').get('href') for item in link]      
    # print(link)    
    return urls    

########### UBAH JUDUL CSV #########
def write_csv(data, url):
    # with open('output.csv', 'w') as csvfile:
    with open('captaino-ring.csv', 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        row = [data['title'], data['price'], data['shipping'], data['total'], data['quantity'], data['desc'], data['img'], url]
        writer.writerow(row)

def login():
    username = "amazonadika@gmail.com"
    password = "kedai123"
    url = "https://www.ebay.com/signin/"
    link = loginbot.startBot(username, password, url)

    return link



def main():
    links = login()
    time.sleep(10)        
    for link in links:        
        data = get_detail_data(get_page(link)) 
        # data['desc'] = get_desc(data['desc'])       #Comment here, if description use template
        write_csv(data, link)        

if __name__ == '__main__':
    main()