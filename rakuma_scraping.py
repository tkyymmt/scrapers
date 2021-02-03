from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import chromedriver_binary
import time
import re


options = Options()

# find @user-data-dir with googling by chrome://version
options.add_argument('user-data-dir=/Users/tky/Library/Application Support/Google/Chrome/')
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get('https://fril.jp/sell')

time.sleep(1)

listing_list = driver.find_element_by_xpath('//*[@id="selling-container"]')
elems = listing_list.find_elements_by_class_name('row')
url_list = []

for elem in elems:
    url_list.append(elem.find_element_by_tag_name('a').get_attribute('href'))

for url in url_list:
    driver.get(url)
    time.sleep(1)

    price_str = driver.find_element_by_class_name('item__value').text
    price_val = re.sub(r"\D", "", price_str)
    new_price = str(int(price_val) - 100)

    edit_btn = driver.find_element_by_xpath( \
        '/html/body/div[2]/div[1]/div/div[2]/div[2]/div/article/div/div[2]/section/div[2]/div/div[1]/p[2]/a')
    edit_btn.click()
    time.sleep(1)

    sell_price = driver.find_element_by_xpath('//*[@id="sell_price"]')
    sell_price.clear()
    time.sleep(1)
    sell_price.send_keys(new_price)
    time.sleep(1)




# 1%の値下げで上位表示されるか検証する




    confirm_button = driver.find_element_by_xpath('//*[@id="confirm"]')
    confirm_button.click()
    time.sleep(1)
    
    submit_btn = driver.find_element_by_xpath('//*[@id="submit"]')
    submit_btn.click()
    time.sleep(3)


driver.quit()