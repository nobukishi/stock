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
driver.get('https://www.google.co.jp')
 
search_bar = driver.find_element(By.NAME, "q")
search_bar.send_keys("python")
search_bar.send_keys(Keys.ENTER)

for elem_h3 in driver.find_elements(By.XPATH,'//a/h3'):
    elem_a = elem_h3.find_element(By.XPATH,'..')  
    print(elem_h3.text)
    print(elem_a.get_attribute('href'))


sleep(10) 