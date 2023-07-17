#How to use: Set WEBPAGE_TARGET, FOLDER_DESTINATION_FILE_NAME, CLASS_NAME_TARGET
#1. Set webpage_target to the web page that holds images you want to 'download'
#2. Set where you want 'downloaded' image to be saved as well as the name. You can find this through inspection through browswer.
# example - 'comics/chapter 1/comic name page' they will be orderd from 1 to end
#3. Set the name of the img tag's class name
# example - chapter-img
#4. Extras - If proxy and have direct link to by pass, set proxys concatenate. Edit to your benefit.

# import webdriver
from selenium import webdriver
# import BY
from selenium.webdriver.common.by import By
#import time
import time

#set const
WEBPAGE_TARGET = ""
FOLDER_DESTINATION_FILE_NAME = '' 
CLASS_NAME_TARGET = ""

#if proxy set it up if not can leave it blank
PROXY_BYPASS_CONCATENATE_ONE = ""
PROXY_BYPASS_CONCATENATE_TWO = ""
IF_PROXY = False
SCROLL_DOWN = True
url_sources_links_list = []

# set options
options = webdriver.ChromeOptions()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

# create webdriver object
driver = webdriver.Chrome(chrome_options=options) # removes automation alert
driver.implicitly_wait(30)

# get target page and redirect back incase if redirected away
for x in range(3):
    driver.get(WEBPAGE_TARGET)
    time.sleep(5)

# store src links
ELEMENTS_IMGS = driver.find_elements(By.CLASS_NAME, CLASS_NAME_TARGET  )

# scroll all the way down until end of page
if SCROLL_DOWN:
    scroll_amout_number = 600
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        for x in range(20):
            driver.execute_script(f'window.scrollTo(0,{scroll_amout_number})')
            scroll_amout_number += 600
            time.sleep(.5)
        time.sleep(3)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

#store url links
for img in ELEMENTS_IMGS:
    #if you have access to the direct img link
    if IF_PROXY:
        by_pass_proxy_link = PROXY_BYPASS_CONCATENATE_ONE + img.get_attribute('src') + PROXY_BYPASS_CONCATENATE_TWO
        url_sources_links_list.append(by_pass_proxy_link)
    else:
        url_src = img.get_attribute('src')
        url_sources_links_list.append(url_src)

# go to download url and screenshot img
page_number = 1
for url_link in url_sources_links_list:
    file_name = FOLDER_DESTINATION_FILE_NAME + str(page_number) + '.png'
    with open(file_name, 'wb') as file:
        driver.get(url_link)
        driver.fullscreen_window()
        time.sleep(10)
        img = driver.find_element(By.TAG_NAME, 'img')
        file.write(img.screenshot_as_png)
    page_number += 1

driver.quit()