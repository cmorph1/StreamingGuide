from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import Settings as S


class Netflix:

    def __init__(self):
        self._driver = None
        self._wait = None

    def login_to_netflix(self):
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
                links_and_titles.append(((films.find_previous("a")["aria-label"]), "www.netflix.com" + (films.find_previous("a")["href"])))
            except:
                continue
        for links in links_and_titles:
            if links[1] == 'www.netflix.com/YourAccount':
                return links_and_titles[1:11]
            else:
                return links_and_titles[0:10]

    def search(self, search: str) -> list:
        self.login_to_netflix()
        self._navigate_to_profile()
        result = self._build_list(search)
        return result

    def _get_url(self):
        return "https://www.netflix.com/gb/login"

    def _get_userinput(self):
        return "userLoginId"

    def _get_username(self):
        return S.NETFLIXUN

    def _get_passinput(self):
        return "password"

    def _get_userpass(self):
        return S.NETFLIXP

    def _get_submitbt(self):
        return '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button'


netflix_search = Netflix()
search_str = input("What would you like to watch? \n")
film_with_link = netflix_search.search(search_str)
print(film_with_link)
