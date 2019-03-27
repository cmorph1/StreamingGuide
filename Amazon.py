from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import Settings as S
from selenium.common.exceptions import NoSuchElementException
import time


class Amazon:

    def __init__(self):
        self._driver = None
        self._wait = None

    def login_to_amazon(self):
        global driver
        driver = webdriver.Chrome()
        global wait
        wait = WebDriverWait(driver, 30)
        driver.get(self._get_url())
        userinput = wait.until(ec.visibility_of_element_located((By.NAME, self._get_userinput())))
        userinput.clear()
        userinput.send_keys(self._get_username())
        userpass = driver.find_element_by_name(self._get_passinput())
        userpass.clear()
        userpass.send_keys(self._get_userpass())
        driver.find_element_by_xpath(self._get_submitbt()).click()

    def _navigate_to_prime(self):
        try:
            useraccount = driver.find_element_by_id("nav-link-yourAccount")
            hover = ActionChains(driver).move_to_element(useraccount)
            hover.perform()
            userprime = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="nav-flyout-yourAccount"]/div[2]/a[15]')))
            userprime.click()
        except NoSuchElementException:
            useraccount = driver.find_element_by_id("nav-link-accountList")
            hover = ActionChains(driver).move_to_element(useraccount)
            hover.perform()
            userprime = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="nav-al-your-account"]/a[15]')))
            userprime.click()

    def _search_prime(self, search: str):
        searchbox = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="twotabsearchtextbox"]')))
        searchbox.clear()
        searchbox.send_keys(str(search))
        driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div').click()
        time.sleep(15)
        html = driver.page_source
        return BS(html, features="lxml")

    def _build_list(self, search: str):
        soup = self._search_prime(search)
        finds = soup.find_all("div", class_="a-section aok-relative s-image-fixed-height")
        links_and_titles = []
        for films in finds:
            try:
                links_and_titles.append(((films.find_next("img")["alt"]), "www.amazon.co.uk" + (films.find_next("a")["href"])))
            except:
                continue
        return links_and_titles

    def search(self, search: str):
        self.login_to_amazon()
        self._navigate_to_prime()
        result = self._build_list(search)
        return result

    def _get_url(self):
        return "https://www.amazon.co.uk/ap/signin?_encoding=UTF8&openid.assoc_handle=gbflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_youraccount_signout%26signIn%3D1%26useRedirectOnSuccess%3D1"

    def _get_userinput(self):
        return "email"

    def _get_username(self):
        return S.AMAZONUN

    def _get_passinput(self):
        return "password"

    def _get_userpass(self):
        return S.AMAZONP

    def _get_submitbt(self):
        return '//*[@id="signInSubmit"]'


amazon_search = Amazon()
search_str = input("What would you like to watch? \n")
results = amazon_search.search(search_str)
print(results)
