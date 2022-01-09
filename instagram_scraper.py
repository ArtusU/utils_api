import time
from urllib.parse import urlparse
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import INSTA_USERNAME, INSTA_PASSWORD


url = "https://www.instagram.com"
browser = webdriver.Chrome()
browser.get(url)

time.sleep(2)
my_button_xpath = "//button[contains(text(), 'Accept All')]"
accept_btn_el = browser.find_element(By.XPATH, my_button_xpath)
accept_btn_el.click()

time.sleep(2)
username_el = browser.find_element(By.NAME, "username")
username_el.send_keys(INSTA_USERNAME)

password_el = browser.find_element(By.NAME, "password")
password_el.send_keys(INSTA_PASSWORD)

time.sleep(1.5)
submit_btn_el = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
submit_btn_el.click()

time.sleep(5)
not_now_xpath = "//button[contains(text(), 'Not Now')]"
not_now_btn_el = browser.find_element(By.XPATH, not_now_xpath)
not_now_btn_el.click()

time.sleep(3)
notification_not_now_xpath = "//button[contains(text(), 'Not Now')]"
notification_not_now_btn_el = browser.find_element(By.XPATH, notification_not_now_xpath)
notification_not_now_btn_el.click()
time.sleep(2)


heather_url = "https://www.instagram.com/gal_gadot/"
browser.get(heather_url)

post_url_pattern = "https://www.instagram.com/p/<post-slug-id>"
post_xpath_str = "//a[contains(@href, '/p/')]"
post_links = browser.find_elements(By.XPATH, post_xpath_str)
post_link_el = None

if len(post_links) > 0:
    post_link_el = post_links[0]

if post_link_el != None:
    post_href = post_link_el.get_attribute("href")
    browser.get(post_href)
    
video_els = browser.find_elements(By.XPATH, "//video")
images_els = browser.find_elements(By.XPATH, "//img")

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)
                    
                    
def scrape_and_save(elements):
    for el in elements:
        url = el.get_attribute('src')
        base_url = urlparse(url).path
        filename = os.path.basename(base_url)
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            continue
        with requests.get(url, stream=True) as r:
            try:
                r.raise_for_status()
            except:
                continue
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
   
                      
# def automate_comment(browser, content="Cool photo!"):
#     time.sleep(3)
#     comment_xpath_str = "//textarea[contains(@placeholder, 'Add a comment')]"
#     comment_el = browser.find_element(By.XPATH, comment_xpath_str)
#     comment_el.send_keys(content)
#     time.sleep(2)
#     submit_btns_xpath = "button[type='submit']"
#     submit_btns_els = browser.find_elements(By.CSS_SELECTOR, submit_btns_xpath)
#     time.sleep(2)
#     for btn in submit_btns_els:
#         try:
#             btn.click()
#         except:
#             pass
        
           
def automate_likes(browser):
    like_heart_svg_xpath = "//*[contains(@aria-label, 'Like')]"
    all_like_hearts_elements = browser.find_elements(By.XPATH, like_heart_svg_xpath)
    max_heart_h = -1
    for heart_el in all_like_hearts_elements:
        h = heart_el.get_attribute("height")
        current_h = int(h)
        if current_h > max_heart_h:
            max_heart_h = current_h
    all_like_hearts_elements = browser.find_elements(By.XPATH, like_heart_svg_xpath)
    for heart_el in all_like_hearts_elements:
        h = heart_el.get_attribute("height")
        if h == max_heart_h or h == f"{max_heart_h}":
            parent_button = heart_el.find_element(By.XPATH, '..')
            time.sleep(2)
            try:
                parent_button.click()
            except:
                pass
            
            
scrape_and_save(video_els)
scrape_and_save(images_els)
# automate_comment(browser, content="Cool photo!")
automate_likes(browser)


