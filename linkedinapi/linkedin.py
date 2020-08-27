import csv
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from django.http import JsonResponse
from rest_framework.decorators import api_view
from selenium.webdriver.firefox.options import Options

HTML_PARSER = 'html.parser'
options = Options()
options.headless = True

@api_view(['POST'])
def check_user(request):
    if request.method == 'POST':
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            return JsonResponse({'message':"username and password requared"},status=400)

        writer = csv.writer(open('testing.csv', 'w')) # preparing csv file to store parsing result later
        writer.writerow(['name', 'job_title', 'schools', 'location', 'ln_url'])

        driver =  webdriver.Firefox(options=options)

        driver.get('https://www.linkedin.com/')

        driver.find_element_by_xpath('//a[text()="Sign in"]').click()

        username_input = driver.find_element_by_name('session_key')
        username_input.send_keys(username)

        password_input = driver.find_element_by_name('session_password')
        password_input.send_keys(password)

        driver.find_element_by_xpath('//button[text()="Sign in"]').click()


        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        except TimeoutException:
            pass

        html = driver.page_source

        soup = BeautifulSoup(html, HTML_PARSER)
        # search_input.send_keys(Keys.RETURN)
        users = soup.find_all(
                'div', {'class': 'profile-rail-card__actor-link t-16 t-black t-bold'})
        # grab all linkedin profiles from first page at Google

        print(users)
        driver.quit()

        if len(users)> 0:
            return JsonResponse({'message':users[0].text})
        else:
            return JsonResponse({'message':"user not found"},status=400)


    else:
        return JsonResponse({'message':"Method Not Allowed"},status=405)