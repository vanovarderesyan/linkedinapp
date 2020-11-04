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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common import action_chains, keys
from campaign.models import (Campaign,SendindUser)
import sys


HTML_PARSER = 'html.parser'
options = Options()
options.headless = True
PROXY = "159.69.199.175:3128"
port = "12345"
chrome_options =webdriver.ChromeOptions()
#chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def local_search(driver,page,campaign_params):
    print('mtav poisk')
    all_page_user = []
    driver.get(str('%s&page='+str(page)) % (campaign_params['linkedin_url']))
    html = driver.page_source
    soup = BeautifulSoup(html, HTML_PARSER)

    
    while len(all_page_user) < campaign_params["count"]:
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 550);")
        time.sleep(5)
        driver.execute_script("window.scrollTo(550, 1150);")
        time.sleep(5)
        driver.execute_script("window.scrollTo(1150, 2500);")
        delay = 5  # seconds
        try:
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        except TimeoutException:
            pass
        users = driver.find_elements_by_css_selector("div.search-result__wrapper")

        for user in users:
            # print(user)
            all_page_user.append(user.find_element_by_css_selector("a.search-result__result-link").get_attribute('href'))
            if len(all_page_user) == 18:
                break
        page = page +1
        driver.get(str('%s&page='+str(page)) % (campaign_params['linkedin_url']))


    # C:\Users\Administrator\Documents\geckodriver-v0.27.0-win32
    # C:\Users\Administrator\AppData\Local\Temp\2\geckodriver-v0.27.0-win32.zip
    JSESSIONID = ""
    for cookie in driver.get_cookies():
        if cookie['name'] == "JSESSIONID":
            JSESSIONID = cookie['value']

    cam = Campaign.objects.create( campaign_id = campaign_params['campaign_id'],message_text=campaign_params['message'],user_id = campaign_params['user_id'],campaign_name =campaign_params['campaign_name'],linkedin_id = campaign_params['linkedin_id'],count =campaign_params["count"] ,linkedin_url =campaign_params['linkedin_url'] )
    for user in all_page_user:
        driver.get(user)
        time.sleep(5)
        linkedin_conect_cret = SendindUser.objects.create(linkedin_user_url=user,campaign=cam)
        linkedin_conect = SendindUser.objects.get(pk=linkedin_conect_cret.pk)
        try:
            driver.find_elements_by_class_name('pv-s-profile-actions')[0].click()

            time.sleep(15)
            driver.find_elements_by_class_name('ml1')[0].click()
            print('------')
            time.sleep(5)
            driver.find_elements_by_class_name('message-anywhere-button')[0].click()

            time.sleep(4)
            linkedin_conect.connect = True
        except:
            try:
                time.sleep(5)
                driver.find_element_by_link_text("Message").click()

                print('gtav')
                #driver.find_elements_by_class_name('message-anywhere-button')[0].click()
            except:
                e = sys.exc_info()[0]
                print( sys.exc_info(),666666 )
        try:

            #textbox = driver.find_element_by_xpath(".//div[@role='textbox']/p[1]")
            print(JSESSIONID)
            conversation_id = ''
            time.sleep(3)
            try:
                a = driver.find_element_by_xpath(".//a[@class='message-anywhere-button pv-s-profile-actions pv-s-profile-actions--message ml2 artdeco-button artdeco-button--2 artdeco-button--primary']")
                conversation_id = a.get_attribute('href').split('Afs_miniProfile%3A')[1].split(')')[0]
            except:
                html = driver.page_source
               # print(html)
                a = driver.find_element_by_xpath(".//h4[@class='msg-overlay-bubble-header__title']/a[1]")
                conversation_id = a.get_attribute('href').split('in/')[1].split('/')[0]
                
            time.sleep(2)
            print('stexa')        
            script = """fetch("https://www.linkedin.com/voyager/api/messaging/conversations?action=create",{
                "headers": {
                    "accept": "application/vnd.linkedin.normalized+json+2.1",
                    "accept-language": "en-US,en;q=0.9,ru;q=0.8",
                    "content-type": "application/json; charset=UTF-8",
                    "csrf-token": %s,
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-li-lang": "ru_RU",
                    "x-li-page-instance": "urn:li:page:d_flagship3_feed;ZsZEQVKQSRqOUb37qIo+Tw==",
                    "x-li-track": JSON.stringify({"clientVersion":"1.7.3536","osName":"web","timezoneOffset":4,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1920,"displayHeight":1080}),
                    "x-restli-protocol-version": "2.0.0"
                },
                "referrer": "https://www.linkedin.com/feed/",
                "referrerPolicy": "strict-origin-when-cross-origin",
                "body": JSON.stringify({'keyVersion': 'LEGACY_INBOX', 'conversationCreate': {'eventCreate': { 'value': {'com.linkedin.voyager.messaging.create.MessageCreate': {'attributedBody': {'text': '%s', 'attributes': []}, 'attachments': []}}}, 'recipients': ['%s'], 'subtype': 'MEMBER_TO_MEMBER'}}),
                "method": "POST",
                "mode": "cors",
                "credentials": "include"
            })"""  %(JSESSIONID ,campaign_params['message'],conversation_id)
        
        
            print(script,'************')
            driver.execute_script(script)
            time.sleep(3)
            print('verj')
            linkedin_conect.message = True
            linkedin_conect.mini_profile = conversation_id
        
            driver.find_element_by_xpath("//button[@class='msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--inverse artdeco-button--1 artdeco-button--tertiary ember-view']").click()

            time.sleep(2) 
                    
        except:
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
        linkedin_conect.save()
    driver.quit()
    return True

def local_statistic(driver,user_id):
    respons= []
    campaigns = Campaign.objects.filter(linkedin_id=user_id)
    print(campaigns,'campaigns',user_id)
    for target_list in campaigns:
        count_seen= 0
        count_reply= 0
        count_connect = 0
        connected_user =  SendindUser.objects.filter(campaign=target_list)
        for target_l in connected_user:
            driver.get(target_l.linkedin_user_url)
            time.sleep(3)
        
            driver.find_elements_by_class_name('message-anywhere-button')[0].click()
            time.sleep(5)
            textbox = driver.find_element_by_xpath(".//div[@role='textbox']/p[1]")
            conversation_id = ''
            time.sleep(3)
            messages = driver.find_elements_by_xpath('.//li[@class="msg-s-message-list__event clearfix"]')[-1]

            try:
                if len(driver.find_elements_by_class_name('pv-s-profile-actions')) == 0 and len(driver.find_elements_by_class_name('pv-s-profile-actions pv-s-profile-actions--connect ml2  artdeco-button artdeco-button--2 artdeco-button--primary artdeco-button--disabled ember-view')) == 0:
                    count_connect = count_connect +1 
            except expression as identifier:
                pass
            if target_l.message:
                try:
                    #msg-s-event-listitem msg-s-event-listitem--last-in-group ember-view
                    href = messages.find_element_by_xpath('.//div[@class="msg-s-message-group__meta"]/a[1]').get_attribute('href')
                    print(href,'hre********************************************f',target_l.linkedin_user_url)
                    if target_l.linkedin_user_url == href:
                        count_reply = count_reply +1
                    messages.find_element_by_xpath('.//div[@class="msg-s-event-listitem__seen-receipts t-12 t-black--light t-normal"]')
                    count_seen = count_seen +1
                except:
                    pass   
                #message ete lenkt exav kardacela ete che urem che
                try:
                    a = driver.find_element_by_xpath(".//a[@class='message-anywhere-button pv-s-profile-actions pv-s-profile-actions--message ml2 artdeco-button artdeco-button--2 artdeco-button--primary']")
                    conversation_id = a.get_attribute('href').split('Afs_miniProfile%3A')[1].split(')')[0]
                except:
                    html = driver.page_source
                    print(html,'*********')
                    a = driver.find_element_by_xpath(".//h4[@class='msg-overlay-bubble-header__title truncate t-14 t-bold t-white pr1']/a[1]")
                    conversation_id = a.get_attribute('href').split('in/')[1].split('/')[0]
        time.sleep(3)

        respons.append({
            "campaign_id":target_list.campaign_id,
            "campaign_name" : target_list.campaign_name,
            'count_sending_message_user':SendindUser.objects.filter(campaign=target_list,message=True).count(),
            'count_sending_connect_user':SendindUser.objects.filter(campaign=target_list,connect=True).count(),
            'count_sending_message_seen_user':count_seen,
            'count_sending_message_reply_user':count_reply,
            'count_sending_connect_accept_user':count_connect,
        })
        # print(target_list)

    driver.quit()
    return respons


@api_view(['POST'])
def secondProcess(request):
    executor_url = request.data.get('executor_url', None)
    url = request.data.get('url', None)
    session_id = request.data.get('session_id', None)
    text = request.data.get('text', None)
    method = request.data.get('type', None)
    campaign_params = request.data.get('campaign_params',{})
    user_id = request.data.get('user_id',None)

    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
 
    driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute
    try:
        driver.get(url) 
    except:
        return JsonResponse({'message':"verification url expired"},status=498)
    
    time.sleep(2)
    try:
        username_input = driver.find_element_by_xpath('.//input[@class="form__input--text input_verification_pin"]')

        username_input.send_keys(int(text)) 
    except:
        return JsonResponse({'message':"Something unexpected happened. Please try again."},status=498) 


    time.sleep(2)
    log_in_button = driver.find_element_by_xpath('.//button[@class="form__submit form__submit--stretch"]')

        #driver.find_element_by_xpath('//button[text()="Sign in"]').click()
    log_in_button.click()
    time.sleep(5)

    err =  driver.find_elements_by_id('email-pin-error')
    if err:
        driver.quit()
        return JsonResponse({'message':"cose is wrong","status":400},status=400)
    else:
        if method == 1:
            req = local_search(driver,1,campaign_params)
            if req:
                return JsonResponse({'message':'ok',"status":200})
            else:
                return JsonResponse({'message':'error',"status":400},status=400)
        if method == 2:
            respons = local_statistic(driver,user_id)
            return JsonResponse({'message':list(respons),"status":200})
            
        
        return JsonResponse({'message':"ok","status":200},status=200)


@api_view(['POST'])
def check_user(request):
    if request.method == 'POST':
        print('check_user')
        #return JsonResponse({'session_id':"test_id",'text':6565,"executor_url":"test_url",'url':"test","code":True,"status":303},status=303)

        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if not username or not password:
            return JsonResponse({'message':"username and password requared","status":400},status=400)

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
        # driver = webdriver.Chrome(seleniumwire_options=option,options=options)
    
        driver= webdriver.Chrome(options=chrome_options)
  
        driver.get('https://www.linkedin.com/')

        driver.find_element_by_xpath('//a[text()="Sign in"]').click()

        username_input = driver.find_element_by_name('session_key')

        username_input.send_keys(username)

        password_input = driver.find_element_by_name('session_password')
        password_input.send_keys(password)
        log_in_button = driver.find_element_by_class_name('btn__primary--large')

        #driver.find_element_by_xpath('//button[text()="Sign in"]').click()
        log_in_button.click()

      
        time.sleep(1)
        try:
            user_code = driver.find_element_by_xpath('.//input[@class="form__input--text input_verification_pin"]')
            if user_code:
                driver.implicitly_wait(280)

                return JsonResponse({'session_id':driver.session_id,'text':6565,"executor_url":driver.command_executor._url,'url':driver.current_url,"code":True,"status":303},status=303)
        except:
            pass

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
        if len(err_code):
            return JsonResponse({'message':'ok1',"status":200})
        try:
            if len(err_password) == 0 and len(err_username) == 0:
                return JsonResponse({'message':'ok',"status":200})
            if len(err_password[0].text) == 0 and len(err_username[0].text )== 0:
                name = driver.find_element_by_xpath('.//div[@class="profile-rail-card__actor-link t-16 t-black t-bold"]')
                
                return JsonResponse({'message':name,"status":200})
            else:
                return JsonResponse({'message':"user not found","status":201},status=201)
        except:
            return JsonResponse({'message':"let's do a quick security check","status":498},status=498)


    else:
        return JsonResponse({'message':"Method Not Allowed","status":405},status=405)


@api_view(['POST'])
def send_message(request):
    if request.method == 'POST':

        user_params = request.data.get('user_params', {})
        username = user_params['username']
        password = user_params['password']
        campaign_params = request.data.get('campaign_params', None)
        if not username or not password:
            return JsonResponse({'message':"username and password requared","status":400},status=400)
        
        if not campaign_params:
            return JsonResponse({'message':"campaign_params requared","status":400},status=400)

        #option = {
        #'proxy': {
        #        'http': 'http://erpufphi-dest:fvxk9prr04j1@209.127.191.180:80',
        #       'https': 'https://erpufphi-dest:fvxk9prr04j1@209.127.191.180:80',
        #       'http': 'http://149.129.100.105:16716',
        #       'https': 'https://149.129.100.105:16716', 
	    #   'no_proxy': ''
        #   }
        #}



        driver= webdriver.Chrome(options=chrome_options)
  
        driver.get('https://www.linkedin.com/')


        driver.find_element_by_xpath('//a[text()="Sign in"]').click()

        username_input = driver.find_element_by_name('session_key')

        username_input.send_keys(username)

        password_input = driver.find_element_by_name('session_password')
        password_input.send_keys(password)
        log_in_button = driver.find_element_by_class_name('btn__primary--large')

        #driver.find_element_by_xpath('//button[text()="Sign in"]').click()
        log_in_button.click()

        time.sleep(1)
        try:
            user_code = driver.find_element_by_xpath('.//input[@class="form__input--text input_verification_pin"]')
            if user_code:
                driver.implicitly_wait(280)

                return JsonResponse({'session_id':driver.session_id,'text':6565,"executor_url":driver.command_executor._url,'url':driver.current_url,"code":True,"status":303},status=303)
        except:
            pass 

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
        if len(err_code):
            return JsonResponse({'message':'ok1',"status":200})
        try:
            if len(err_password[0].text) == 0 and len(err_username[0].text )== 0:
               return JsonResponse({'message':'ok2',"status":200})
            else:
               return JsonResponse({'message':"user not found","status":201},status=201)
        except:
            return JsonResponse({'message':"let's do a quick security check","status":201},status=201)

    else:
        return JsonResponse({'message':"Method Not Allowed","status":405},status=405)

@api_view(['POST'])
def get_statistic(request,user_id):
    """
    docstring
    """
    print(user_id,'get_statistic',request.data)

    HTML_PARSER = 'html.parser'
    username = request.data.get('username',None)
    password = request.data.get('password',None)
    if not username or not password:
        return JsonResponse({'message':"username and password requared","status":400},status=400)
    
    driver= webdriver.Chrome(options=chrome_options)
    driver.get('https://www.linkedin.com/')
    time.sleep(3)

    driver.find_element_by_xpath('//a[text()="Sign in"]').click()
    username_input = driver.find_element_by_name('session_key')
    username_input.send_keys(username)
    time.sleep(2)

    password_input = driver.find_element_by_name('session_password')
    password_input.send_keys(password)
    driver.find_element_by_xpath('//button[text()="Sign in"]').click()
    time.sleep(2)

    try:
        user_code = driver.find_element_by_xpath('.//input[@class="form__input--text input_verification_pin"]')
        if user_code:
            driver.implicitly_wait(280)

            return JsonResponse({'session_id':driver.session_id,'text':6565,"executor_url":driver.command_executor._url,'url':driver.current_url,"code":True,"status":303},status=303)
    except:
        pass
    respons = local_statistic(driver,user_id)
    return JsonResponse({'message':list(respons),"status":200})

@api_view(['POST'])
def rekursiv_serach(request):
    if request.method == 'POST':
        print('rekursiv_serach')

        page=1
        all_page_user = []
        #,'https://www.linkedin.com/in/svetlana-petrosyan-2abb24137/','https://www.linkedin.com/in/lusine-sargsyan-9b00b8172/','https://www.linkedin.com/in/anoushik-sahakyan-756ab8181/'
        # all_page_user = ['https://www.linkedin.com/in/lilit-baghdasaryan-330034b3/','https://www.linkedin.com/in/tsovinar-martirosyan/','https://www.linkedin.com/in/svetlana-petrosyan-2abb24137/','https://www.linkedin.com/in/lusine-sargsyan-9b00b8172/','https://www.linkedin.com/in/anoushik-sahakyan-756ab8181/']


        HTML_PARSER = 'html.parser'
        user_params = request.data.get('user_params', {})
        print(user_params,'*******************',request.data)
        username = user_params['username']
        password = user_params['password']
        campaign_params = request.data.get('campaign_params', None)
        if not username or not password:
            return JsonResponse({'message':"username and password requared","status":400},status=400)
        
        if not campaign_params:
            return JsonResponse({'message':"campaign_params requared","status":400},status=400)


        driver= webdriver.Chrome(options=chrome_options)
  
        driver.get('https://www.linkedin.com/')
        
        time.sleep(3)
        driver.find_element_by_xpath('//a[text()="Sign in"]').click()
        username_input = driver.find_element_by_name('session_key')
        username_input.send_keys(username)
        time.sleep(2)

        password_input = driver.find_element_by_name('session_password')
        password_input.send_keys(password)

        driver.find_element_by_xpath('//button[text()="Sign in"]').click()
        time.sleep(2)
        try:
            user_code = driver.find_element_by_xpath('.//input[@class="form__input--text input_verification_pin"]')
            if user_code:
                driver.implicitly_wait(280)

                return JsonResponse({'session_id':driver.session_id,'text':6565,"executor_url":driver.command_executor._url,'url':driver.current_url,"code":True,"status":303},status=303)
        except:
            pass


        req = local_search(driver,page,campaign_params)
        if req:
            return JsonResponse({'message':'ok',"status":200})
        else:
            return JsonResponse({'message':'error',"status":400},status=400)
    else:
        return JsonResponse({'message':"Method Not Allowed","status":405},status=405)
