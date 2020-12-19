
'''
Name: index.py
Purpose: To alert user when a products price drops to expected value on ecommerce stores like 
MI, Amazon, flipkart,oneplus
Authors:
    Sree Rukmini Tummu
    Nithin Tata
    Ram kiran
    Fatima leenah shah
Please read attached readme file and install requied packages using "pip install -r requirements.txt"
'''
import os
import time
import re
import sys
os.environ['WDM_LOG_LEVEL'] = '0'
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from senemail import send_email

#Class used to print colured lineso on terminal
class clr:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


data={}
def dataassign(k,v):
    '''
        Function takes key value and add to data dictonary
    '''
    global data
    data[k]=v


def mi():
    '''
        Function to check product price on MI website
    '''
    print("URL belongs to MI website")
    dataassign("website","MI")
    driver.get(url)
    pricenow=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="information-section__product-price"]'))).text.split('\n')[0].replace(",","")
    time.sleep(5)
    dataassign("status","out of stock") if 'Notify Me' in driver.page_source else dataassign("status","in stock")
    dataassign("price",pricenow)
    dataassign("productname",driver.find_element_by_xpath('//h1[@class="information-section__product-title"]/span').text)

def flipkart():
    '''
        Function to check product price on Flipkart website
    '''
    print("URL belongs to flipkart website")
    dataassign("website","flipkart")
    driver.get(url)
    dataassign("status","out of stock") if 'This item is currently out of stock' in driver.page_source else dataassign("status","in stock")
    nowprice=driver.find_element_by_xpath('//div[@class="_30jeq3 _16Jk6d"]').text.replace(',','')
    dataassign("price",nowprice)
    dataassign("productname",driver.find_element_by_xpath('//span[@class="B_NuCI"]').text)

def amazon():
        '''
            Function to check product price on amazon website
        '''
        print("URL belongs to amazon website")
        dataassign("website","amazon")
        driver.get(url)
        nowprice=(driver.find_element_by_xpath('//span[@id="priceblock_ourprice" or @id="priceblock_dealprice" ]').text.replace(",","").replace('₹',"").strip().split(".")[0])
        nowprice = re.findall(r'\d+', nowprice)
        nowprice=int(nowprice[0])
        dataassign("price",nowprice)
        dataassign("productname",driver.find_element_by_xpath('//span[@id="productTitle"]').text)
        dataassign("status","out of stock") if 'buy now' in driver.page_source else dataassign("status","in stock")


def oneplus():
    '''
        Function to check product price on Oneplus website
    '''
    print("URL belongs to oneplus website")
    dataassign("website","oneplus")
    driver.get(url)
    name=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="font-headline-2"]'))).text
    dataassign("productname",name)
    pricenow=int(driver.find_element_by_xpath('//a[contains(text(),"Price Details")]/preceding-sibling::span').text.replace("₹","").replace(',',''))
    dataassign("status","out of stock") if 'Out of stock' in driver.page_source else dataassign("status","in stock")
    dataassign("price",pricenow)


def checkprice(interval):
    '''
        Function to check product price in recursive mode, 
        interval: intiger value in minutes for sleep time
    '''
    #print(f"Thanks, We will check product price again in {interval} minutes at {time.ctime(time.time()+interval*60)}")
    time.sleep(interval*60)
    #print(data)
    globals()[r[0]]()
    data["price"]=data["price"].replace("₹","").replace(',',"")
    driver.save_screenshot("driver.png")
    #print("data:",data)
    try:
        int(data["price"])
    except:
        print(f"failed to extract price from {globals()[r[0]]} website, will try in next run")
    if int(data["price"]) > int(data["expectedPrice"]):
        print(f'{clr.OKCYAN}Sorry your {data["website"]} product, named {data["productname"]} is priced at {clr.ENDC}{clr.BOLD}{data["price"]}{clr.ENDC}{clr.OKCYAN}, We will check product price again in {interval} minutes at {time.ctime(time.time()+interval*60)}{clr.ENDC}')  
        checkprice(interval)
    else:
        print("Sending email, please wait")
        send_email(data)



#initialization for chrome driver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_argument("--window-size=1420,1080")
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

try:
    acceptedstores=["amazon","flipkart","mi","oneplus"]
    #Taking user inputs
    print(f"{clr.OKGREEN}Please enter product URL from online stores {','.join(acceptedstores)} :{clr.ENDC}",end=" ")
    url=input()
    dataassign("url",url)

    print(f"{clr.OKGREEN}Please enter your email id for alerts:{clr.ENDC}", end=" ")
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' #to verify input email id is valid or not
    receiver_mail=input()
    if(re.search(regex,receiver_mail)):  
        print("Valid Email")  
        dataassign("receiver_mail",receiver_mail)
    else:  
        print("Invalid Email, please restart program and enter valid email address")
        sys.exit()


    print(f"{clr.OKGREEN}Please enter expected price:{clr.ENDC}",end=" ") #input expected price from user
    dataassign("expectedPrice",input())
    r=[(i) for i in url.split('.') if i in acceptedstores]

    #take url, check url belongs to which website and call respective function in single line
    print(f"Store not available. Please select from available store {','.join(acceptedstores)}") if len(r)==0 else globals()[r[0]]()

    #remving special characters from price for converting to integer
    data["price"]=str(data["price"]).replace('₹','').replace(",","")

    #comparing live product price with expected product price
    if int(data["price"]) > int(data["expectedPrice"]):
        print(f'{clr.OKBLUE}Sorry your {data["website"]} product, named {data["productname"]} is priced at {clr.ENDC}{clr.BOLD}{data["price"]}{clr.ENDC}{clr.FAIL}, do you want to have an alert when price got doropped?{clr.ENDC}')  
        print(f"{clr.OKGREEN}if YES type 1:{clr.ENDC}",end=" ")
        var=input()
        #Requesting user for alert
        if var=='1': 
            print(f"Setting alert")
            print(f"{clr.OKGREEN}Please enter time interval in minutes to check price:{clr.ENDC}", end=" ")
            interval=int(input())
            print(f"Setting up alert...., first check will be at {time.ctime(time.time()+interval*60)}")
            checkprice(interval)
        else:
            print("Thanks for using our script. See you soon")
            send_email(data) #send email with details and screenshot
    else:
        print("Please wait, Sending email....")
        send_email(data) #send email with details and screenshot
        print(f'{clr.FAIL}Hola.. selected {data["website"]} product, named {data["productname"]} is available at price {clr.ENDC}{clr.BOLD}{data["price"]}{clr.ENDC}{clr.FAIL}.{clr.ENDC}')  
except Exception as e:
    print(f"Sorry there was an unexpected error {e}, please try after sometime")