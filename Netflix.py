from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import Settings as s

Search = input("What would you like to watch? \n")
driver = webdriver.Chrome()
driver.get("https://www.netflix.com/gb/login")
wait = WebDriverWait(driver, 30)


def logintonetflix():
    username = driver.find_element_by_name("userLoginId")
    username.clear()
    username.send_keys(s.Netflixun)
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(s.Netflixp)
    driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button').click()


def navigatetoprofile():
    yourprofile = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="appMountPoint"]/div/div/div/div/div[2]/div/div/ul/li[1]/div/a/div/div')))
    yourprofile.click()


def searchnetflix():
    searchicon = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'icon-search')))
    hover = ActionChains(driver).move_to_element(searchicon)
    hover.perform()
    searchicon.click()
    searchbox = driver.switch_to.active_element
    searchbox.send_keys(str(Search))
    time.sleep(10)
    html = driver.page_source
    return BS(html, features="lxml")


def buildlist():
    logintonetflix()
    navigatetoprofile()
    soup = searchnetflix()
    finds = soup.find_all("a", class_="slider-refocus")
    LinksAndTitles = []
    for linkandtitle in finds:
        try:
            LinksAndTitles.append(((linkandtitle.find_previous("a")["aria-label"]), "www.netflix.com" + (linkandtitle.find_previous("a")["href"])))
        except:
            continue
    for links in LinksAndTitles:
        if links[1] == 'www.netflix.com/YourAccount':
            return LinksAndTitles[1:11]
        else:
            return LinksAndTitles[0:10]


print(buildlist())
