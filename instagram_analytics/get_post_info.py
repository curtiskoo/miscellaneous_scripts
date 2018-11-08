from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
import time
from bs4 import BeautifulSoup
import os
from pprint import pprint
import re
import sys
#from InstagramAPI import InstagramAPI
import json

master = "insta_map.json"

def export_json(fn, data):
    with open(fn, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=3)
    print("[Exported]: {}".format(fn))

def load_json(fn):
    with open(fn) as f:
        data = json.load(f)
    print("[Imported]: {}".format(fn))
    return data


if not(os.path.isfile(master)):
    export_json(master, {})

master_dic = load_json(master)

target = sys.argv[1]
url = "https://www.instagram.com/{}".format(target)
acc = 1
browser = webdriver.Chrome("/Users/curtiskoo/Desktop/python1/chromedriver")
browser.get(url)
elems = browser.find_elements_by_xpath("//*[@class='eLAPa']")
elems[0].click()

existing_keys = []
if target in master_dic:
    existing_keys = list(master_dic[target].keys())

print("Existing Records: {}".format(len(existing_keys))) #comment out

def key_right(browser):
    actions = ActionChains(browser)
    actions.send_keys(Keys.RIGHT)
    actions.perform()


def get_shortcode(url):
    x = url.split("/")
    ind = x.index('p') + 1
    x = x[ind]
    return x


def get_html_source(html, b=None):
    shortcode = get_shortcode(b)
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find_all("script", {'type': 'text/javascript'})
    temp = list(filter(lambda x: "shortcode_media" in str(x), soup))
    # pprint(temp)
    if len(temp) != 1:
        print("Error at Post: {} | Found shortcode_media: {}".format(acc, len(temp)))
        return
    tt = temp[0].get_text()
    regex = "{(.+?)}"
    find = re.findall(regex, tt)
    find = list(filter(lambda x: shortcode in str(x), find))
    if len(find) != 1:
        print("Error at Post: {} | Found find: {}".format(acc, len(find)))
        print(find)
        return
    find = find[0].replace(":", ",").replace("\"", "").split(",")
    post_id = find[find.index("id") + 1]
    #print(post_id)
    return post_id

prev = None
def get_url_lst():
    global prev
    lst_url = []
    right_button = "//a[@class='HBoOv coreSpriteRightPaginationArrow']"
    while True:
        try:
            rb = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, right_button)))
            time.sleep(1)
            elem = browser.find_element_by_xpath('//a[@class="c-Yi7"]')
            sc = elem.get_attribute('href')
            #print(sc)
            #print(prev)
            #while prev == sc:
            #    if browser.current_url not in lst_url and browser.current_url not in existing_keys:
            #        lst_url.append(browser.current_url)
            #    key_right(browser)
            #    #lst_url.append(browser.current_url)
            #    pass
            #print("{} | {}".format(get_shortcode(browser.current_url), get_shortcode(sc)))
            if browser.current_url not in lst_url and get_shortcode(browser.current_url) not in existing_keys:
                lst_url.append(browser.current_url)
            #print(prev, browser.current_url)
            # browser.refresh()
            # html = browser.page_source
            # soup = get_html_source(html)
            #prev = browser.current_url
            #key_right(browser)
            if prev != len(lst_url):
                prev = len(lst_url)
                print(len(lst_url))
            rb.click()
            # acc += 1
        except TimeoutException:
            print("Done")
            break
    return lst_url

lst_url = get_url_lst()
pprint(lst_url)
print(len(lst_url))

def get_all_id(lst_url):
    lst_id = []
    acc = 1
    for x in lst_url:
        browser.get(x)
        try:
            id = get_html_source(browser.page_source, x)
        except:
            print("Error at: {}".format(x))
            id = None
        lst_id.append(id)
        acc += 1
    return lst_id

id_lst = get_all_id(lst_url)
lst_url = list(map(lambda x: get_shortcode(x), lst_url))
diczip = dict(zip(lst_url, id_lst))



if target not in master_dic:
    master_dic[target] = diczip
else:
    tempval = master_dic[target].copy()
    tempval.update(diczip)
    master_dic[target] = tempval

export_json(master, master_dic)

"""
api = InstagramAPI("", "")
api.login()

for x in id_lst:
    api.mediaInfo(x)
    info = api.LastJson
    print(info)
"""
