from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

#username = '6cinnamon'
#username = 'hepsq'

# get usernames
with open('profile_names.csv', 'rb') as csvfile:
    cupidreader = csv.reader(csvfile, delimiter=';')
    for row in cupidreader:
        usernames = row

#usernames = ['tennis286']
        
browser = webdriver.Firefox()

# Login
browser.get('https://www.okcupid.com')
assert 'OkCupid' in browser.title

actions = webdriver.common.action_chains.ActionChains(browser)

elem = browser.find_element_by_id('open_sign_in_button')  # Find the search box
actions.move_to_element(elem).click(elem).perform()

name_box = browser.find_element_by_id('login_username')  # Find name box
name_box.send_keys('stephen.roger@outlook.com')

name_box = browser.find_element_by_id('login_password')  # Find password box
name_box.send_keys('RogerRoger'  + Keys.RETURN)

time.sleep(1)

for username in usernames:
    print 'Checking out ' + username


    browser.get('http://www.okcupid.com/profile/' + username + '/questions')

    time.sleep(3)

    # Get how many questions are answered in total
    num_questions_string = browser.find_element_by_id('question_comparison').text
    num_questions = int(num_questions_string.split()[3])
    print num_questions

    # Initialize
    question_ids = []
    question_contents = []
    question_answers = []

    time.sleep(3) 

    for startrange in range(1, num_questions+1, 10):
        browser.get('http://www.okcupid.com/profile/' + username + '/questions?low=' + str(startrange))

        time.sleep(3) 
    
        # get ids of questions
        question_header = browser.find_element_by_class_name('pages_content')
        question_list = question_header.find_elements_by_xpath("*")
        # Check if have questions
        first_question = question_list[0]
        if first_question.get_attribute('id') != 'questions_bs':
            question_ids_new = [int(question.get_attribute('data-qid')) for question in question_list]
            question_ids = question_ids + question_ids_new
        else:
            question_ids_new = []

        #print question_ids

        # get questions
        for id in question_ids_new:
            question_contents.append(browser.find_element_by_id('qtext_' + str(id)).text.encode('utf-8'))

        #print question_contents

        # get their answers
        for id in question_ids_new:
            # Check if answered
            check_answered = browser.find_element_by_id('question_' + str(id))
            if 'not_answered' not in check_answered.get_attribute('class'):
                question_answers.append(browser.find_element_by_id('answer_target_' + str(id)).text.encode('utf-8'))
            else:
                question_answers.append('NaN')

        #print question_answers

    # Write to csv file
    with open('questions_' + username + '.csv', 'wb') as csvfile:
        cupidwriter = csv.writer(csvfile, delimiter=';')
        cupidwriter.writerow(['sep=;'])
        cupidwriter.writerow([''] + question_ids)
        cupidwriter.writerow([''] + question_contents)
        cupidwriter.writerow([username] + question_answers)
