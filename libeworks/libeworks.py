from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import requests
import os

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
    print('Signing in libecity')
    time.sleep(3)

def get_search_words():
    search_words = []
    file_path = os.path.dirname(__file__) + '/search_words.txt'
    with open(file_path, 'r') as f:
        search_words = f.read().split('\n')

    return search_words

notified_jobs_file = os.path.dirname(__file__) + '/notified_jobs.txt'

def get_notified_urls():
    notified_job_urls = []
    with open(notified_jobs_file, 'r') as f:
        notified_job_urls = f.read().split('\n')

    return notified_job_urls

def search_new_jobs():
    # リベシティワークスへ
    driver.get('https://works.libecity.com')
    time.sleep(5)
    # 新着順(default)、専用案件を隠す(default)、 募集終了を隠す
    hide_finish = driver.find_element(By.ID, 'hideFinish')
    hide_finish.click()
    time.sleep(3)
    # ジョブ検索
    job_urls = []
    search_words = get_search_words()
    search_url = 'https://works.libecity.com/search?'
    print('Searching new jobs')
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
                if job_url not in job_urls:
                    job_urls.append(job_url)
    except:
        print('Some exception has occured while searching new jobs')
    
    # search jobs that is not notified yet
    new_job_urls = []
    notified_job_urls = get_notified_urls()
    for job_url in job_urls:
        if job_url not in notified_job_urls:
            new_job_urls.append(job_url)
    return new_job_urls

# notify me new jobs
def notify_me(new_job_urls):
    new_job_urls_str = '\n'.join(new_job_urls)
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    payload = {
        "content"       : new_job_urls_str,
    }
    print('Sending notification to Discord')
    res = requests.post(webhook_url, json=payload)
    print(res.status_code)

def append_notified_jobs(new_job_urls):
    with open(notified_jobs_file, 'a') as f:
        newline_new_job_urls = '\n'.join(new_job_urls)
        f.write(newline_new_job_urls)
    

def main():
    signin_to_libecity()
    new_job_urls = search_new_jobs()
    driver.close()
    if new_job_urls:
        notify_me(new_job_urls)
        append_notified_jobs(new_job_urls)

if __name__ == "__main__":
    main()
