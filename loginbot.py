from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
 
# Get the path of chromedriver which you have install
 
def startBot(username, password, url):     
    # giving the path of chromedriver to selenium webdriver
    options = Options()
    # options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 15)
     
    # opening the website  in chrome.
    driver.get(url)
     
    time.sleep(15)
    # find the id or name or class of
    # username by inspecting on username input
    driver.find_element(by=By.NAME, value="userid").send_keys(username)
     
    # click on submit
    driver.find_element(by=By.NAME, value="signin-continue-btn").click()

    # import time
    time.sleep(8)
    # find the password by inspecting on password input
    driver.find_element(by=By.NAME, value="pass").send_keys(password)
     # click on submit
    driver.find_element(by=By.NAME, value="sgnBt").click()

    time.sleep(20)
    my_links = []
    driver.get('https://www.ebay.com/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn=captaino-ring&store_cat=0&store_name=captainoring&_oac=1&_sop=15')

    try:
        time.sleep(5)
        class_names = ['s-item__link']
        links = [driver.find_elements(by=By.CLASS_NAME, value=class_name) for class_name in class_names if len(driver.find_elements(by=By.CLASS_NAME, value=class_name)) != 0 ][0]
        # print(links)
        for link in links:
            #only download links that starts with http
            if(link.get_attribute("href")[:4].lower() in ["http"]):
                print("[INFO] , %s"%(link.get_attribute("href")))
                my_links.append(link.get_attribute("href"))                
    except:
        print("[INFO] Unable to get link")
    
    return my_links
    
 
# Driver Code
# Enter below your login credentials
# username = "authenpineung@gmail.com"
# password = "Kedai110"
 
# URL of the login page of site
# which you want to automate login.
# url = "https://www.ebay.com/signin/"
 
# Call the function
# startBot(username, password, url)