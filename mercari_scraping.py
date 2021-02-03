from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import chromedriver_binary
import time
import re


options = Options()

# find the path with searching by chrome://version
options.add_argument('user-data-dir=/Users/tky/Library/Application Support/Google/Chrome/')
#options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get('https://www.mercari.com/jp/mypage/listings/listing/')

listing_list = driver.find_element_by_id('mypage-tab-transaction-now')
elems = listing_list.find_elements_by_tag_name('a')
edit_url_list = []
big_discount_list = []


for elem in elems:
    status = elem.find_element_by_class_name('mypage-item-status')
    if status.text == '公開停止中':
        continue

    item_title = elem.find_element_by_class_name('mypage-item-text')
    likes = elem.find_element_by_tag_name('span')
    if 10 <= int(likes.text) and  '【値下げ】' in item_title.text:
        continue

    product_url = elem.get_attribute('href')
    product_id = re.search(r'm\d+', product_url)
    edit_url = 'https://www.mercari.com/jp/sell/edit/' + product_id.group()

    if 10 <= int(likes.text):
        big_discount_list.append(edit_url)
    else:
        edit_url_list.append(edit_url)


for edit_url in edit_url_list:
    driver.get(edit_url)
    time.sleep(1)

    sell_price = driver.find_element_by_xpath("//*[@id='sell-container']/div/div/form[1]/div[5]/div/ul/li[1]/div/div/div/input")
    new_price = int(sell_price.get_attribute("value")) - 100

    sell_price.clear()
    time.sleep(1)
    sell_price.send_keys(str(new_price))
    time.sleep(1)

    submit_button = driver.find_element_by_xpath('//*[@id="sell-container"]/div/div/form[2]/div/button')
    submit_button.click()
    time.sleep(3)


for edit_url in big_discount_list:
    driver.get(edit_url)
    time.sleep(1)

    title_elem = driver.find_element_by_xpath('//*[@id="sell-container"]/div/div/form[1]/div[2]/div[1]/div/input')
    new_title = '【値下げ】' + title_elem.get_attribute('value')

    title_elem.clear()
    time.sleep(1)
    title_elem.send_keys(new_title)
    time.sleep(1)

    sell_price = driver.find_element_by_xpath("//*[@id='sell-container']/div/div/form[1]/div[5]/div/ul/li[1]/div/div/div/input")
    new_price = int(sell_price.get_attribute("value")) * 0.9

    sell_price.clear()
    time.sleep(1)
    sell_price.send_keys(str(new_price))
    time.sleep(1)

    submit_button = driver.find_element_by_xpath('//*[@id="sell-container"]/div/div/form[2]/div/button')
    submit_button.click()
    time.sleep(3)


driver.quit()