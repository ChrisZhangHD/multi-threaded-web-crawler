import urllib.error
from urllib import request

import requests as requests
from googlesearch import search


def get_data_from_request(url):
    try:
        # print(url)
        req = request.Request(url)
        response = request.urlopen(req)
        http_message = response.info()
        content_type = http_message.get_content_type()
        res = []
        if "text/html" == content_type:
            html_data = response.read().decode('utf-8')
            page_size = response.headers["content-length"]
            res.append(html_data)
            res.append((page_size if page_size else "0") + "Bytes")
        return res
    except urllib.error.HTTPError as e:
        print("Http Error Code: " + str(e.code))
    except urllib.error.URLError as e:
        print("URL Error: " + str(e.reason))
    except UnicodeDecodeError as e:
        print("UnicodeDecodeError: " + str(e.reason))


def search_from_google(keywords):
    seeds = set()
    for url in search(keywords, tld="co.in", num=12, stop=10, pause=2):
        seeds.add(url)
    return seeds


if __name__ == "__main__":
    # key_words = ["nyu", "dog"]
    # links = set()
    # api_key = "AIzaSyA7aWYZkb27pfHB4gSDSbvuqeZYzWzEeSk"
    # program_search_engine_id = "243c4562e747901f1"
    # google_api_url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s" \
    #                  % (api_key, program_search_engine_id, "+".join(key_words))
    # data = get_data_from_request(google_api_url)
    # json_data = json.loads(data)
    # item_list = json_data["items"]
    # for item in item_list:
    #     links.add(item["link"])
    # print(links)
    url = "https://twitter.com/nyutandon/status/1436422494399963161?lang=bg"
    get_data_from_request(url)
