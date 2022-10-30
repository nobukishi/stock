from selenium import webdriver
from time import sleep
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
#driver = webdriver.Chrome('./chromedriver')
driver = webdriver.Chrome(options=options)
driver.get('https://kabutan.jp/warning/?mode=2_1&market=1')
 
div = driver.find_element(By.CLASS_NAME, "warning_contents")
elem_tables = div.find_elements(By.CLASS_NAME,'stock_table st_market')

i = 0
while True:
    i = i + 1

    for elem_h3 in driver.find_elements(By.XPATH,'//tbody/tr'):
        elem_a = elem_h3.find_element(By.XPATH,'td')  
        print(elem_h3.text,elem_a.text)
    next_link = driver.find_element(By.CLASS_NAME,'pnnext')
    driver.get(next_link.get_attribute('href'))
   
    if i > 4:
        break

