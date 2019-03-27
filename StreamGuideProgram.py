from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
import time
import sqlite3

class StreamGuide:

    def __init__(self):
        self._driver = None
        self._wait = None

    def login(self):
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

    def _build_list(self, search: str):
        pass

    def search(self, search: str):
        if self._driver is None:
            self.login()

    def _get_url(self):
        pass

    def _get_userinput(self):
        pass

    def _get_username(self):
        pass

    def _get_passinput(self):
        pass

    def _get_userpass(self):
        pass

    def _get_submitbt(self):
        pass


class Amazon(StreamGuide):

    def __init__(self):
        super().__init__()

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
        return links_and_titles[0:10]

    def search(self, search: str) -> list:
        super().search(search)
        self._navigate_to_prime()
        result = self._build_list(search)
        return result

    def _get_url(self):
        return "https://www.amazon.co.uk/ap/signin?_encoding=UTF8&openid.assoc_handle=gbflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26action%3Dsign-out%26path%3D%252Fgp%252Fyourstore%252Fhome%26ref_%3Dnav_youraccount_signout%26signIn%3D1%26useRedirectOnSuccess%3D1"

    def _get_userinput(self):
        return "email"

    def _get_username(self):
        conn = sqlite3.connect("userdetails.sqlite")
        for streamer, username, password in conn.execute("SELECT * FROM userdetails WHERE streamer = 'Amazon Prime'"):
            return username
        conn.close()

    def _get_passinput(self):
        return "password"

    def _get_userpass(self):
        conn = sqlite3.connect("userdetails.sqlite")
        for streamer, username, password in conn.execute("SELECT * FROM userdetails WHERE streamer = 'Amazon Prime'"):
            return password
        conn.close()

    def _get_submitbt(self):
        return '//*[@id="signInSubmit"]'


class Netflix(StreamGuide):

    def __init__(self):
        super().__init__()

    def _navigate_to_profile(self):
        yourprofile = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="appMountPoint"]/div/div/div/div/div[2]/div/div/ul/li[1]/div/a/div/div')))
        yourprofile.click()

    def _search_netflix(self, search: str):
        searchicon = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'icon-search')))
        hover = ActionChains(driver).move_to_element(searchicon)
        hover.perform()
        searchicon.click()
        searchbox = driver.switch_to.active_element
        searchbox.send_keys(str(search))
        time.sleep(5)
        html = driver.page_source
        return BS(html, features="lxml")

    def _build_list(self, search: str):
        soup = self._search_netflix(search)
        finds = soup.find_all("a", class_="slider-refocus")
        links_and_titles = []
        for films in finds:
            try:
                links_and_titles.append(((films.find_previous("a")["aria-label"]),
                                         "www.netflix.com" + (films.find_previous("a")["href"])))
            except:
                continue
        for links in links_and_titles:
            if links[1] == 'www.netflix.com/YourAccount':
                return links_and_titles[1:11]
            else:
                return links_and_titles[0:10]

    def search(self, search: str) -> list:
        super().search(search)
        self._navigate_to_profile()
        result = self._build_list(search)
        return result

    def _get_url(self):
        return "https://www.netflix.com/gb/login"

    def _get_userinput(self):
        return "userLoginId"

    def _get_username(self):
        conn = sqlite3.connect("userdetails.sqlite")
        for streamer, username, password in conn.execute("SELECT * FROM userdetails WHERE streamer = 'Netflix'"):
            return username
        conn.close()

    def _get_passinput(self):
        return "password"

    def _get_userpass(self):
        conn = sqlite3.connect("userdetails.sqlite")
        cursed = conn.cursor()
        for streamer, username, password in cursed.execute("SELECT * FROM userdetails WHERE streamer = 'Netflix'"):
            return password
        cursed.close()
        conn.close()

    def _get_submitbt(self):
        return '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button'


class NowTV(StreamGuide):

    def __init__(self):
        super().__init__()

    def _navigate_to_nowtv(self):
        yourprofile = wait.until(ec.visibility_of_element_located((By.XPATH, '//*[@id="ib-section-header-region"]/div/div[2]/div/div[2]/nav/ul/li[7]/div/a')))
        yourprofile.click()

    def _search_nowtv(self, search: str):
        searchicon = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'search-suggest-input')))
        hover = ActionChains(driver).move_to_element(searchicon)
        hover.perform()
        time.sleep(5)
        searchicon.click()
        searchbox = driver.switch_to.active_element
        searchbox.send_keys(str(search))
        time.sleep(10)
        html = driver.page_source
        return BS(html, features="lxml")

    def _build_list(self, search: str):
        soup = self._search_nowtv(search)
        unlisted = soup.find("ul", class_="search-suggest-list focused")
        try:
            finds = unlisted.find_all("li", "search-suggest-list-item")
            links_and_titles = []
            for films in finds:
                links_and_titles.append((films.find_next("span", class_="search-suggest-result--asset").text,
                                         ("www.nowtv.com" + (films.find_next("a")["href"]))))
            return links_and_titles
        except:
            return "Either your search was incorrect or Now TV doesn't have what you are looking for"

    def search(self, search: str) -> list:
        super().search(search)
        self._navigate_to_nowtv()
        result = self._build_list(search)
        return result

    def _get_url(self):
        return "https://www.nowtv.com/gb/sign-in?successUrl=https%3A%2F%2Fwww.nowtv.com%2Fhome%2Fexisting"

    def _get_userinput(self):
        return "userIdentifier"

    def _get_username(self):
        conn = sqlite3.connect("userdetails.sqlite")
        for streamer, username, password in conn.execute("SELECT * FROM userdetails WHERE streamer = 'Now TV'"):
            return username
        conn.close()

    def _get_passinput(self):
        return "password"

    def _get_userpass(self):
        conn = sqlite3.connect("userdetails.sqlite")
        for streamer, username, password in conn.execute("SELECT * FROM userdetails WHERE streamer = 'Now TV'"):
            return password
        conn.close()

    def _get_submitbt(self):
        return '//*[@id="mount"]/div/div/div[2]/div[2]/section/div/section[1]/div/div/div/form/div[3]/button'

if __name__ == "__main__":
    amazon_search = Amazon()
    netflix_search = Netflix()
    nowtv_search = NowTV()
    search_str = input("What would you like to watch? \n")
    results = amazon_search.search(search_str), netflix_search.search(search_str), nowtv_search.search(search_str)
    for services in results:
        print(services)
