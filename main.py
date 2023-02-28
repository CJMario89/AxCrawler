from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--log-level=1")
driver = webdriver.Chrome(options=options)


oldLinks = []
newLinks = []


def getInfoOneRound():
  driver.get('https://app.axieinfinity.com/marketplace/')
  print(driver)
  wait = WebDriverWait(driver, 60000)
  print(wait)
  # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='RecentSales_Slide__FEile']")))
  sold_items = driver.find_element(By.CSS_SELECTOR, "[class='RecentSales_Slide__FEile']").find_elements(By.TAG_NAME, 'a')
  print(sold_items)
  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='RecentSales_Slide__FEile']")))
  print(wait)


  sold_items = driver.find_element(By.CSS_SELECTOR, "[class='RecentSales_Slide__FEile']").find_elements(By.TAG_NAME, 'a')

  i = 0
  for sold_item in sold_items:
    if(sold_item.get_attribute('href') not in oldLinks):
      newLinks.append(sold_item.get_attribute('href'))

  newLinks.reverse()

  for i in range(len(newLinks)):
    data = []
    driver.get(newLinks[i])
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='AxieAbout_AxieAbout__xqNKh']")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='SaleHistory_SaleHistory__ltMpK']")))
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='special-tag-module_content__npQsV']")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup)
    axie = soup.find('span', class_='special-tag-module_content__npQsV').getText()
    axieClass = soup.find('div', class_='AxieAbout_AxieAbout__xqNKh').find('div', class_='capitalize').getText()
    bodys = soup.find_all('div', class_='BodyPartInfo_Name__e3q4L')
    bread_count = soup.find('div', class_='AxieAbout_AxieAbout__xqNKh').find('div', 'leading-20').find('span').getText()
    price = soup.find('div', class_='SaleHistory_SaleHistory__ltMpK').find('h5').getText()
  
    
    data.append(axie)
    data.append(str(datetime.now()).replace(' ', 'T'))
    data.append(axieClass)
    data.append(bread_count.replace(' ', ''))
    data.append(price.replace(' ', ''))
    for body in bodys:
      data.append(body.getText().replace(' ', ''))



    with open('axies.csv', 'a') as file:
      writer = csv.writer(file)
      writer.writerows([data])

while 1:
  getInfoOneRound()
  for link in newLinks:
    oldLinks.append(link)
    if(len(oldLinks) > 30):
      oldLinks.pop(0)
  newLinks = []
  time.sleep(300)
  



