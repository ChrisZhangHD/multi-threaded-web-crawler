import urllib.parse as urlparse  # 用来拼接url
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):

    def __init__(self, base_url):
        super().__init__()
        self.base_url = str(base_url)
        self.url_set = set()
        self.ignore_url_ends = ["index.htm", "index.html", "index.jsp", "main.html", ".jpg", ".exe", ".pdf"]

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        for key, val in attrs:
            if "href" == key:
                self.insert_url_set(val)

    def handle_startendtag(self, tag, attrs):
        for key, val in attrs:
            if "href" == key:
                self.insert_url_set(val)

    def insert_url_set(self, url):
        new_full_url = urlparse.urljoin(self.base_url, str(url))
        can_insert = 1
        for url_ends in self.ignore_url_ends:
            if new_full_url.endswith(url_ends):
                can_insert = 0
                break
        if can_insert:
            self.url_set.add(new_full_url)
