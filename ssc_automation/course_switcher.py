from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

time1 = time.time()

landing = 'https://courses.students.ubc.ca/cs/main?pname=regi_sections&tname=regi_sections'
login = 'https://cas.id.ubc.ca/ubc-cas/login'

user = ""
pwd = ""

driver = webdriver.Chrome()
driver.get(login)

elem = driver.find_element_by_name("username")
elem.send_keys(user)
elem = driver.find_element_by_id("password")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)

driver.get(landing)
#time.sleep(1)
submit = driver.find_element_by_xpath('//input[@name="IMGSUBMIT"]')
submit.click()
#time.sleep(1)
trs = driver.find_elements_by_xpath('//table[@class="table table-striped section-summary"]//tbody/tr')

#source = sys.argv[1]
target = sys.argv[1]

trs = list(filter(lambda x: "CPSC 121" in x.text and "Laboratory" in x.text, trs))[0]
print("Current Course: {}".format(trs.text))

checkbox = trs.find_element_by_xpath('.//input')
checkbox.click()

driver.find_element_by_xpath('//input[@value="Switch Selected Section"]').click()

boxes = driver.find_elements_by_xpath('//tbody/tr//input')
boxes = list(filter(lambda x: target in x.get_attribute("value"), boxes))[0]
boxes.click()

switchsections = driver.find_element_by_xpath('//input[@value="Switch Sections"]').click()

time2 = time.time()
print("[Execution Time]: {} seconds".format(time2-time1))