from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

browser = webdriver.Chrome()

RATING_NUMBER = {
    'E-':1, 'E':2, 'E+':3,
    'D-':4, 'D':5, 'D+':6,
    'C-':7, 'C':8, 'C':9,
    'B-':10, 'B':11, 'B+':12,
    'A-':13, 'A':14, 'A+':15
}

NUMBER_TO_TEXT = {
    1:'E', 2:'D', 3:'C', 4:'B', 5:'A'
}

def login(username, password):
    browser.get('https://ust.space/login')
    if browser.current_url == 'https://ust.space/home':
        return
    form_username = browser.find_element_by_id('username')
    form_username.clear()
    form_username.send_keys(username)
    form_password = browser.find_element_by_id('password')
    form_password.clear()
    form_password.send_keys(password)
    form_password.send_keys(Keys.RETURN)
    if browser.current_url == 'https://ust.space/home':
        return
    else:
        raise ValueError('Error on login.')

def request_review_page_soup(course_code):
    course_code = course_code.upper()
    browser.get('https://ust.space/review/{0}'.format(course_code))
    if browser.current_url == 'https://ust.space/review':
        raise ValueError('Course {0} doesn\'t exist.'.format(course_code))


    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '//ul[@class="menu-content"]/li[2]'))
    )
    return BeautifulSoup(browser.page_source, 'html.parser')

def get_course_rating(soup):
    tag = soup.find('div', class_='course-review-statistics').ul
    return [x.get_text() for x in tag.find_all('span')]

def get_instructor_list(soup):
    tag = soup.find('li', attrs={'data-key':'filterInstructor'}).ul
    return [x['data-text'] for x in tag.find_all('li', attrs={'data-text':True})]

def request_instructor_page_soup(name):
    first_menu = browser.find_element_by_xpath('//li[@data-key="filterInstructor"]')
    second_menu = browser.find_element_by_xpath('//li[@data-text="{0}"]'.format(name))
    ActionChains(browser).click(first_menu).click(second_menu).perform()


    def second_menu_is_active(browser):
        second_menu_ = browser.find_element_by_xpath('//li[@data-text="{0}"]'.format(name))
        return second_menu_ if 'active' in second_menu_.get_attribute('class') else False
    WebDriverWait(browser, 10).until(second_menu_is_active)
    return BeautifulSoup(browser.page_source, 'html.parser')

def get_instructor_review(soup):
    sum1 = [0,0,0,0]
    sum2 = [0,0,0,0]
    all_reviews = soup.find_all('div', class_='course-review-record')
    reviews_count = len(all_reviews)
    for x in all_reviews:
        rating_container = x.div.ul
        ratings = [int(x['class'][1][-1]) for x in rating_container.find_all('span')]
        for i in range(4):
            sum1[i] += ratings[i]
            sum2[i] += ratings[i]**2
    average = [round(x/reviews_count, 2) for x in sum1]
    average_text = [NUMBER_TO_TEXT[round(x)] for x in average]
    variance = [round(sum2[i]/reviews_count-average[i]**2, 2) for i in range(4)]
    return average_text, average, variance

def quit():
    browser.quit()
