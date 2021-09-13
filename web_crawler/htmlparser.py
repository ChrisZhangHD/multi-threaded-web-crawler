import urllib.parse as urlparse  # 用来拼接url
from html.parser import HTMLParser

import requestdata


class MyHTMLParser(HTMLParser):

    def __init__(self, base_url):
        super().__init__()
        self.base_url = str(base_url)
        self.url_set = set()
        self.ignore_url_ends = ["index.htm", "index.html", "index.jsp", "main.html"]

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        for key, val in attrs:
            if "href" == key:
                self.insert_url_set(val)

    def handle_startendtag(self, tag, attrs):
        # for key, val in attrs:
        #     if "href" == key:
        #         new_full_url = urlparse.urljoin(self.base_url, val)
        #         self.url_set.add(new_full_url)
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

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)
    #
    # def handle_data(self, data):
    #     print("Encountered some data  :", data)


if __name__ == '__main__':
    # url = "https://www.runoob.com/python/python-reg-expressions.html"
    url = "https://www.akc.org/dog-breeds/smallest-dog-breeds/"
    res = requestdata.get_data_from_request(url)
    # print(data)
    parser = MyHTMLParser(url)
    # parser.feed("<link href='www.baidu.com/html'/>")
    parser.feed(res[0])
    print(parser.url_set)
