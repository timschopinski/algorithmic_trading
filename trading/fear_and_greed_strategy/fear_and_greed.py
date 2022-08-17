from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests


def get_fear_and_greed_index_without_js():
    URL = "https://alternative.me/crypto/fear-and-greed-index/"
    r = requests.get(URL)

    soup = BeautifulSoup(r.content, 'html.parser')
    content = soup.find('div', attrs={'class': 'fng-circle'})
    index = int(content.text)
    return index


def get_fear_and_greed_index_with_js():
    """ getting the Fear and greed index from the look into bitcoin website """

    url = 'https://www.lookintobitcoin.com/charts/bitcoin-fear-and-greed-index/'
    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(url)

    time.sleep(10)
    htmlSource = driver.page_source
    soup = BeautifulSoup(htmlSource)
    data = soup.find_all(class_="number")
    index = int(data[0].get_text().split('/')[0])
    return index


def main():
    # index = get_fear_and_greed_index()
    # print(index)
    pass


if __name__ == '__main__':
    main()