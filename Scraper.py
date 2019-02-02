from bs4 import BeautifulSoup as bs
import http.client
import urllib

def generate_url_and_connection(domain: str, path: str, is_https: bool, credentials: dict):

    if 1 == is_https:
        conn = http.client.HTTPSConnection(domain)
    else:
        conn = http.client.HTTPConnection(domain)

    # params = urllib.parse.urlencode(credentials)

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" + \
                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    headers = {'User-Agent': user_agent}

    if path is not None:
        # conn.request("POST", path, params, headers=headers)
        conn.request("GET", path, headers=headers)
    else:
        conn.request("GET", "/", headers=headers)  # params

    rs = conn.getresponse()
    source = rs.read()
    return bs(source, 'lxml')


credential_dict = {"email": "", "password": ""}
soup = generate_url_and_connection('www.evilhat.com','/home/category/evilhat,ehp-blogs,our-news,dresden-files-rpg-game-news,race-to-adventure-2,fate-core/', True, credential_dict)

finds = soup.find_all("li", class_="menu-item-object-post")
LinksAndTitles = []

def buildlist():
    LinksAndTitles = []
    for linkandtitle in finds:
        LinksAndTitles.append(((linkandtitle.find_next(string=True)), (linkandtitle.find("a")["href"])))
    return LinksAndTitles

print(buildlist())


# https://www.amazon.co.uk/Prime-Video/b/ref=nav_youraccount_piv?ie=UTF8&node=3280626031

# userLoginId
# password
# post

# now tv
# userIdentifier
# password
# get
