import sys
from time import sleep
from matplotlib import pyplot as plt
import urllib.request as urlr
from bs4 import BeautifulSoup as soup



def grab_price_km(start_url):
    pages = [] 
    #load index page
    pages.append(urlr.urlopen(start_url))
    #parse index page
    pages[0] = soup(pages[0], 'html.parser')

    cars_link = pages[0].find_all('ul', attrs={'class':'motor'})
    cars = []
    for c in cars_link:
        p = c.find('a', attrs={'class':'buyNowPrice'})
        km = p
        p = p.text
        p = p[1:].replace(',', '')
        p = int(p)

        km = km['href']
        km = 'https://www.trademe.co.nz/motors' + km
        km = urlr.urlopen(km)
        km = soup(km, 'html.parser')
        km = km.find_all('span', attrs={'class':'motors-attribute-value'})
        for i in km:
            if 'km' in i.text:
                km = i.text
                break
        km = km[:-2].replace(',','')
        try:
            km = int(km)
        except:
            continue

        sleep(0.03)
        cars.append((p, km))
    return cars

def main():
    car_data = grab_price_km(sys.argv[1])
    x_val = [x[1] for x in car_data]
    y_val = [x[0] for x in car_data]
    
    plt.plot(x_val, y_val, 'or')
    plt.xlabel('km')
    plt.ylabel('price')
    plt.show()


if __name__ == '__main__':
    main()
