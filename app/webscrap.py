from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

class GetWashingMachineDetail:

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    driver.get('https://www.flipkart.com/washing-machines/pr?sid=j9e,abm,8qx&page=1')
    content = driver.page_source
    soup = BeautifulSoup(content,'html.parser')

    def __init__(self):
        self.products=[] #product name store in this list
        self.prices=[] #product price store in this list
        self.ratings=[] #product ratings store in this list

    def getPageNo(self):
        for nav_div in self.soup.find_all('div',attrs={'class':'_2MImiq'}):
            return int(nav_div.find('span').text.split('of')[-1])

    def getProductInfo(self):
        for i in range(1,int(self.getPageNo())): # Get Current page no
            current_url=self.driver.current_url.replace(self.driver.current_url.split('&')[-1].split('=')[-1],str(i))
            self.driver.get(current_url) #change request url
            content = self.driver.page_source
            soup = BeautifulSoup(content,'html.parser')

            for a in self.soup.findAll('a',href=True, attrs={'class':'_1fQZEK'}):
                name=a.find('div', attrs={'class':'_4rR01T'})
                price=a.find('div', attrs={'class':'_30jeq3 _1_WHN1'})
                rating=a.find('div', attrs={'class':'_3LWZlK'})

                self.products.append(name.text)
                self.prices.append(price.text)
                self.ratings.append(rating.text)

        df = pd.DataFrame({'Product Name':self.products,'Price':self.prices,'Rating':self.ratings})
        df.to_csv('products.csv', index=False, encoding='utf-8')

wminfo=GetWashingMachineDetail()
print(wminfo.getProductInfo())