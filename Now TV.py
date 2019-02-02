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
driver.get("https://www.nowtv.com/gb/sign-in?successUrl=https%3A%2F%2Fwww.nowtv.com%2Fhome%2Fexisting")
wait = WebDriverWait(driver, 30)


def logintonowtv():
    username = wait.until(EC.visibility_of_element_located((By.NAME, "userIdentifier")))
    username.clear()
    username.send_keys(s.Nowtvun)
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(s.Nowtvp)
    driver.find_element_by_xpath('//*[@id="mount"]/div/div/div[2]/div[2]/section/div/section[1]/div/div/div/form/div[3]/button').click()


def navigatetonowtv():
    yourprofile = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ib-section-header-region"]/div/div[2]/div/div[2]/nav/ul/li[7]/div/a')))
    yourprofile.click()


def searchnowtv():
    searchicon = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'search-suggest-input')))
    hover = ActionChains(driver).move_to_element(searchicon)
    hover.perform()
    time.sleep(5)
    searchicon.click()
    searchbox = driver.switch_to.active_element
    searchbox.send_keys(str(Search))
    time.sleep(14)
    html = driver.page_source
    return BS(html, features="lxml")


def buildlist():
    logintonowtv()
    navigatetonowtv()
    soup = searchnowtv()
    unlisted = soup.find("ul", class_="search-suggest-list focused")
    try:
        finds = unlisted.find_all("li", "search-suggest-list-item")
        LinksAndTitles = []
        for linkandtitle in finds:
            LinksAndTitles.append(((linkandtitle.find_next("span", class_="search-suggest-result--asset").text),
                                   ("www.nowtv.com" + (linkandtitle.find_next("a")["href"]))))
        return LinksAndTitles
    except:
        return "Either your search was incorrect or Now TV doesn't have what you are looking for"


print(buildlist())