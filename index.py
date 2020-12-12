
'''
https://www.mi.com/in/buy/product/redmi-9a?gid=4203700001
https://www.flipkart.com/stag-2-star-playset-bat-3-balls-table-tennis-kit/p/itmf5ftfzymbty6m?pid=KITF5FQQNGQSRZZS&lid=LSTKITF5FQQNGQSRZZSHTC7RK&marketplace=FLIPKART&srno=b_1_1&otracker=hp_omu_Deals%2Bof%2Bthe%2BDay_2_4.dealCard.OMU_KA7FMDZ0SZ8Y_3&otracker1=hp_omu_SECTIONED_neo%2Fmerchandising_Deals%2Bof%2Bthe%2BDay_NA_dealCard_cc_2_NA_view-all_3&fm=neo%2Fmerchandising&iid=98e20af6-d739-470a-b9d7-15fb0a7492a5.KITF5FQQNGQSRZZS.SEARCH&ppt=browse&ppn=browse&ssid=r8s6fwimsg0000001607785000104
https://www.amazon.in/OnePlus-Mirror-Black-128GB-Storage/dp/B085J1CPD1/ref=sr_1_1?dchild=1&pf_rd_i=22301453031&pf_rd_m=A1K21FY43GMZF8&pf_rd_p=3139e855-12fb-466d-b0ca-4bcaa0c663bd&pf_rd_r=Z6ZGRHNJ64B2952RWFEX&pf_rd_s=merchandised-search-2&pf_rd_t=101&qid=1607785039&sr=8-1

'''
import os
import time
os.environ['WDM_LOG_LEVEL'] = '0'
try:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
except:
    os.system("python -m pip install selenium")
    os.system("python -m pip install webdriver_manager")

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
    global data
    data[k]=v
def mi():
    print("URL belongs to MI website")
    dataassign("website","MI")
    driver.get(url)
    pricenow=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="information-section__product-price"]'))).text.split('\n')[0].replace(",","")
    dataassign("status","out of stock") if 'Notify Me' in driver.page_source else dataassign("status","in stock")
    dataassign("price",pricenow)
    dataassign("productname",driver.find_element_by_xpath('//h1[@class="information-section__product-title"]/span').text)

def flipkart():
      print("URL belongs to flipkart website")
      dataassign("website","flipkart")
      driver.get(url)
      dataassign("status","out of stock") if 'This item is currently out of stock' in driver.page_source else dataassign("status","in stock")
      nowprice=driver.find_element_by_xpath('//div[@class="_30jeq3 _16Jk6d"]').text.replace(',','')
      dataassign("price",nowprice)
      dataassign("productname",driver.find_element_by_xpath('//span[@class="B_NuCI"]').text)

def amazon():
        print("URL belongs to amazon website")
        dataassign("website","amazon")
        driver.get(url)
        nowprice=int(driver.find_element_by_xpath('//span[@id="priceblock_ourprice" or @id="priceblock_dealprice" ]').text.replace(",","").replace('₹',"").strip().split(".")[0])
        dataassign("price",nowprice)
        dataassign("productname",driver.find_element_by_xpath('//span[@id="productTitle"]').text)
        dataassign("status","out of stock") if 'buy now' in driver.page_source else dataassign("status","in stock")

def oneplus():
    print("URL belongs to oneplus website")
    dataassign("website","oneplus")
    driver.get(url)
    pricenow=int(driver.find_element_by_xpath('//a[contains(text(),"Price Details")]/preceding-sibling::span').text.replace("₹",""))
    dataassign("status","out of stock") if 'Out of stock' in driver.page_source else dataassign("status","in stock")
    dataassign("price",pricenow)

def checkprice(interval):
    print(f"Thanks, We will check product price again in {interval} minutes at {time.ctime(time.time()+interval*60)}")
    time.sleep(interval*60)
    globals()[r[0]]()
    if int(data["price"]) > int(data["expectedPrice"]):
        print(f'{clr.FAIL}Sorry your {data["website"]} product, named {data["productname"]} is priced at {clr.ENDC}{clr.BOLD}{data["price"]}{clr.ENDC}{clr.FAIL}, do you want to have an alert when price got doropped?{clr.ENDC}')  
    else:
        checkprice(interval)


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
acceptedstores=["amazon","flipkart","mi","oneplus"]
print(f"Please enter product URL from online stores {','.join(acceptedstores)} :",end=" ")
url=input()
dataassign("url",url)
print(f"Please enter expected price:",end=" ")
dataassign("expectedPrice",input())
r=[(i) for i in url.split('.') if i in acceptedstores]
print(f"Store not available. Please select from available store {','.join(acceptedstores)}") if len(r)==0 else globals()[r[0]]()
data["price"]=str(data["price"]).replace('₹','')
if int(data["price"]) > int(data["expectedPrice"]):
    print(f'{clr.FAIL}Sorry your {data["website"]} product, named {data["productname"]} is priced at {clr.ENDC}{clr.BOLD}{data["price"]}{clr.ENDC}{clr.FAIL}, do you want to have an alert when price got doropped?{clr.ENDC}')  
    print("if YES type 1:")
    var=input()
    if var=='1':
        print("Setting alert")
        print("Please enter time interval in minutes to check price:", end=" ")
        interval=int(input())
        checkprice(interval)
    else:
        print("Thanks")
else:
    print("in price limit")