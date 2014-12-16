from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv 

repeat_num = 10

browser = webdriver.Firefox()

browser.get('https://www.okcupid.com')
assert 'OkCupid' in browser.title

actions = webdriver.common.action_chains.ActionChains(browser)

elem = browser.find_element_by_id('open_sign_in_button')  # Find the search box
actions.move_to_element(elem).click(elem).perform()

name_box = browser.find_element_by_id('login_username')  # Find name box
name_box.send_keys('stephen.roger@outlook.com')

name_box = browser.find_element_by_id('login_password')  # Find password box
name_box.send_keys('RogerRoger'  + Keys.RETURN)

#browse_matches = browser.find_element_by_partial_link_text('Browse Matches')  # Find password box
#actions.move_to_element(browse_matches).click(browse_matches).perform()

time.sleep(3)

profile_names = []

for i in range(0,30):
    print i
    browser.get('http://www.okcupid.com/match?filter1=0,34&filter2=2,18,38&filter3=3,25&filter4=5,2678400&filter5=1,1&locid=0&timekey=1&matchOrderBy=SPECIAL_BLEND&custom_search=0&fromWhoOnline=0&mygender=m&update_prefs=1&sort_type=0&sa=1&using_saved_search=&count=54')
    time.sleep(3)


    
    profile_infos = browser.find_elements_by_class_name('profile_info')
    for profile_info in profile_infos:
        profile_names.append(profile_info.find_element_by_tag_name('a').text.encode('utf-8'))
        #print profile_info.find_element_by_tag_name('a').text

    profile_names = list(set(profile_names))
    
# Write to csv file
with open('profile_names.csv', 'wb') as csvfile:
    cupidwriter = csv.writer(csvfile, delimiter=';')
    cupidwriter.writerow(['sep=;'])
    cupidwriter.writerow(profile_names)
