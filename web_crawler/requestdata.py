import socket
import urllib.error
from urllib import request

from googlesearch import search


def get_data_from_request(url):
    try:
        timeout = 1
        socket.setdefaulttimeout(timeout)
        req = request.Request(url)
        response = request.urlopen(req)
        http_message = response.info()
        content_type = http_message.get_content_type()
        html_data = ""
        if "text/html" == content_type:
            html_data = response.read().decode('utf-8')
        response.close()
        return html_data
    except urllib.error.HTTPError as e:
        print(url + " Http Error Code: " + str(e.code))
        return
    except urllib.error.URLError as e:
        print(url + " URL Error: " + str(e.reason))
        return
    except socket.error:
        print(url + " socket time out ")
        return
    except UnicodeDecodeError as e:
        print(url + " UnicodeDecodeError: " + str(e.reason))
        return
    except Exception:
        return


def search_from_google(keywords):
    seeds = set()
    for url in search(keywords, tld="co.in", num=12, stop=10, pause=2):
        seeds.add(url)
    return seeds
