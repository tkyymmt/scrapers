from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import requests
import os


#from selenium.webdriver.chrome.service import Service
#import chromedriver_autoinstaller
#from pyvirtualdisplay import Display
#display = Display(visible=0, size=(800, 800))  
#display.start()
#chromedriver_autoinstaller.install()
#chrome_options = webdriver.ChromeOptions()    
#options = [
   #"--window-size=1200,1200",
    #"--ignore-certificate-errors"
    ##"--headless",
#]
#for option in options:
    #chrome_options.add_argument(option)

    
#driver = webdriver.Chrome(options = chrome_options)

from get_chrome_driver import GetChromeDriver
get_driver = GetChromeDriver()
get_driver.install()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)



def signin_to_libecity():
    signin_url = 'https://libecity.com/signin'
    driver.get(signin_url)
    email_form = driver.find_element(By.XPATH, "//input[@placeholder='メールアドレス']")
    password_form = driver.find_element(By.XPATH, "//input[@type='password']")
    email = os.environ['EMAIL']
    password = os.environ['PASSWORD']
    email_form.send_keys(email)
    password_form.send_keys(password)
    login_button = driver.find_element(By.XPATH, "//button[@type='button']")
    login_button.click()
    time.sleep(3)

def search_new_jobs():
    # リベシティワークスへ
    driver.get('https://works.libecity.com')
    time.sleep(5)
    # 新着順(default)、専用案件を隠す(default)、 募集終了を隠す
    hide_finish = driver.find_element(By.ID, 'hideFinish')
    hide_finish.click()
    time.sleep(3)
    # ジョブ検索
    new_job_urls = []
    search_words = ['開発', 'エンジニア']
    search_url = 'https://works.libecity.com/search?'
    try:
        for word in search_words:
            query_param = 'keyword=' + word
            driver.get(search_url + query_param)
            time.sleep(3)

            job_boxes = driver.find_elements(By.CLASS_NAME, 'jobBox')
            for job_box in job_boxes:
                caption = job_box.find_element(By.CLASS_NAME, 'caption')
                a_tag = caption.find_element(By.TAG_NAME, 'a')
                job_url = a_tag.get_attribute('href')
                if job_url in new_job_urls:
                    continue
                new_job_urls.append(job_url)
    except:
        print('Some exception has occured while searching jobs')
    
    return new_job_urls


# notify me new jobs
def notify_me(new_job_urls):
    new_job_urls_str = '\n'.join(new_job_urls)
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    payload = {
        "content"       : new_job_urls_str,
    }
    res = requests.post(webhook_url, json=payload)
    print(res.status_code)


def main():
    signin_to_libecity()
    new_job_urls = search_new_jobs()
    driver.close()
    notify_me(new_job_urls)

if __name__ == "__main__":
    main()