from bs4 import BeautifulSoup as bs
import http.client

def generate_url_and_connection(domain: str, path: str, is_https: bool):

    if 1 == is_https:
        conn = http.client.HTTPSConnection(domain)
    else:
        conn = http.client.HTTPConnection(domain)

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" + \
                 "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    headers = {'User-Agent': user_agent}

    if path is not None:
        conn.request("GET", path, headers=headers)
    else:
        conn.request("GET", "/", headers=headers)

    rs = conn.getresponse()
    source = rs.read()

    return bs(source, 'lxml')

soup = generate_url_and_connection('www.netflix.com', '/gb/', True)
print(soup)