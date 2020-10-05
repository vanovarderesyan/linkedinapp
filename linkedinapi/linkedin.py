import csv

from parsel import Selector
from seleniumwire import webdriver
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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common import action_chains, keys



HTML_PARSER = 'html.parser'
options = Options()
options.headless = True
PROXY = "107.172.229.117:12345"
port = "12345"

@api_view(['POST'])
def check_user(request):
    if request.method == 'POST':
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            return JsonResponse({'message':"username and password requared"},status=400)

        writer = csv.writer(open('testing.csv', 'w')) # preparing csv file to store parsing result later
        writer.writerow(['name', 'job_title', 'schools', 'location', 'ln_url'])
            
        # option = {
        # 'proxy': {
        # #        'http': 'http://erpufphi-dest:fvxk9prr04j1@209.127.191.180:80',
        # #       'https': 'https://erpufphi-dest:fvxk9prr04j1@209.127.191.180:80',
        #         'http': 'http://149.129.100.105:16716',
        #         'https': 'https://149.129.100.105:16716', 
	    #     'no_proxy': ''
        #     }
        # }
        # driver = webdriver.Firefox(seleniumwire_options=option,options=options)
        driver = webdriver.Firefox()
  
        driver.get('https://www.linkedin.com/')

        driver.find_element_by_xpath('//a[text()="Sign in"]').click()

        username_input = driver.find_element_by_name('session_key')

        username_input.send_keys(username)

        password_input = driver.find_element_by_name('session_password')
        password_input.send_keys(password)
        log_in_button = driver.find_element_by_class_name('btn__primary--large')

        #driver.find_element_by_xpath('//button[text()="Sign in"]').click()
        log_in_button.click()


        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        except TimeoutException:
            pass

        html = driver.page_source
        print(html)
        soup = BeautifulSoup(html, HTML_PARSER)
        # search_input.send_keys(Keys.RETURN)
        users = soup.find_all(
                'div', {'class': 'profile-rail-card__actor-link t-16 t-black t-bold'})
        # grab all linkedin profiles from first page at Google

        print(users)
        driver.quit()
        err_password = soup.find_all(
                'div', {'id': 'error-for-password'})
        print(len(err_password))
        err_username = soup.find_all('div',{'id':'error-for-username'})
        print(len(err_username))
        err_code = soup.find_all('input',{'id':'input__email_verification_pin'})
        print(err_code,'code info')
        if err_code:
            return JsonResponse({'message':'ok'})
        try:
            if len(err_password[0].text) == 0 and len(err_username[0].text )== 0:
               return JsonResponse({'message':'ok'})
            else:
               return JsonResponse({'message':"user not found"},status=201)
        except:
            return JsonResponse({'message':"let's do a quick security check"},status=201)

    else:
        return JsonResponse({'message':"Method Not Allowed"},status=405)


@api_view(['POST'])
def send_message(request):
    if request.method == 'POST':

        user_params = request.data.get('user_params', {})
        username = user_params['username']
        password = user_params['password']
        campaign_params = request.data.get('campaign_params', None)
        if not username or not password:
            return JsonResponse({'message':"username and password requared"},status=400)
        
        if not campaign_params:
            return JsonResponse({'message':"campaign_params requared"},status=400)

        driver = webdriver.Firefox()
  
        driver.get('https://www.linkedin.com/')

        driver.find_element_by_xpath('//a[text()="Sign in"]').click()

        username_input = driver.find_element_by_name('session_key')

        username_input.send_keys(username)

        password_input = driver.find_element_by_name('session_password')
        password_input.send_keys(password)
        log_in_button = driver.find_element_by_class_name('btn__primary--large')

        #driver.find_element_by_xpath('//button[text()="Sign in"]').click()
        log_in_button.click()


        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        except TimeoutException:
            pass

        html = driver.page_source
        print(html)
        soup = BeautifulSoup(html, HTML_PARSER)
        # search_input.send_keys(Keys.RETURN)
        users = soup.find_all(
                'div', {'class': 'profile-rail-card__actor-link t-16 t-black t-bold'})
        # grab all linkedin profiles from first page at Google

        print(users)
        driver.quit()
        err_password = soup.find_all(
                'div', {'id': 'error-for-password'})
        print(len(err_password))
        err_username = soup.find_all('div',{'id':'error-for-username'})
        print(len(err_username))
        err_code = soup.find_all('input',{'id':'input__email_verification_pin'})
        print(err_code,'code info')
        if err_code:
            return JsonResponse({'message':'ok'})
        try:
            if len(err_password[0].text) == 0 and len(err_username[0].text )== 0:
               return JsonResponse({'message':'ok'})
            else:
               return JsonResponse({'message':"user not found"},status=201)
        except:
            return JsonResponse({'message':"let's do a quick security check"},status=201)

    else:
        return JsonResponse({'message':"Method Not Allowed"},status=405)