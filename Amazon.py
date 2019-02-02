from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Settings as s


Search = input("What would you like to watch? \n")
driver = webdriver.Chrome()
driver.get("https://www.amazon.co.uk/ap/signin?_encoding=UTF8&openid.assoc_handle=gbflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_youraccount_signout%26signIn%3D1%26useRedirectOnSuccess%3D1")
wait = WebDriverWait(driver, 20)


def logintoamazon():
    username = driver.find_element_by_name("email")
    username.clear()
    username.send_keys(s.Amazonun)
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(s.Amazonp)
    driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()


def navigatetoprime():
    youraccount = driver.find_element_by_id("nav-link-yourAccount")
    hover = ActionChains(driver).move_to_element(youraccount)
    hover.perform()
    yourprime = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="nav-flyout-yourAccount"]/div[2]/a[15]')))
    yourprime.click()


def searchprime():
    searchbox = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))
    searchbox.clear()
    searchbox.send_keys(str(Search))
    driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div').click()
    html = driver.page_source
    return BS(html, features="lxml")


def buildlist():
    logintoamazon()
    navigatetoprime()
    soup = searchprime()
    finds = soup.find_all("a", class_="a-link-normal a-text-normal")
    LinksAndTitles = []
    for linkandtitle in finds:
        LinksAndTitles.append(((linkandtitle.find_next(string=True)), (linkandtitle.find_next("a")["href"])))
    return LinksAndTitles[:20:2]


print(buildlist())
