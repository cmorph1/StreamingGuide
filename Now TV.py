from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import Settings as S


class NowTV:

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
        self.login()
        self._navigate_to_nowtv()
        result = self._build_list(search)
        return result

    def _get_url(self):
        return "https://www.nowtv.com/gb/sign-in?successUrl=https%3A%2F%2Fwww.nowtv.com%2Fhome%2Fexisting"

    def _get_userinput(self):
        return "userIdentifier"

    def _get_username(self):
        return S.NOWTVUN

    def _get_passinput(self):
        return "password"

    def _get_userpass(self):
        return S.NOWTVP

    def _get_submitbt(self):
        return '//*[@id="mount"]/div/div/div[2]/div[2]/section/div/section[1]/div/div/div/form/div[3]/button'

if __name__ == "__main__":
    nowtv_search = NowTV()
    search_str = input("What would you like to watch? \n")
    results = nowtv_search.search(search_str)
    print(results)
