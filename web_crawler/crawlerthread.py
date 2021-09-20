import socket
import urllib.robotparser
from concurrent.futures import ThreadPoolExecutor
from urllib.error import URLError

import htmlparser
import requestdata


class CrawlerThread:

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.robot_map = {}

    def submit_task(self, cur_page):
        return self.executor.submit(self.put_url_to_pq_task, cur_page)

    def put_url_to_pq_task(self, cur_page):
        cur_link = cur_page.page_link
        # deal with CGI scripts
        if "cgi" in cur_link:
            return
        rp = self.get_robot_parser(cur_page.domain)
        if rp and not rp.can_fetch("*", cur_link):
            return
        cur_html_data = requestdata.get_data_from_request(cur_link)
        if not cur_html_data:
            return
        cur_page_size = len(cur_html_data)
        result_sentence = "Time: %s; Page: %s; Score: %.3f; Size: %dB; Depth:%d" % \
                          (cur_page.download_time, cur_link, cur_page.score, cur_page_size, cur_page.depth)
        # print(result_sentence)
        parser = htmlparser.MyHTMLParser(cur_link)
        parser.feed(cur_html_data)
        return [parser.url_set, cur_page, result_sentence]

    def get_robot_parser(self, domain):
        try:
            if domain not in self.robot_map:
                rp = urllib.robotparser.RobotFileParser()
                # print("domain: " + domain)
                # print("robot: " + parse.urljoin(domain, '/robots.txt'))
                rp.set_url("https://" + domain + '/robots.txt')
                rp.read()
                self.robot_map[domain] = rp
            return self.robot_map[domain]
        except URLError as e:
            self.robot_map[domain] = None
            return self.robot_map[domain]
        except socket.timeout as e:
            return
        except UnicodeDecodeError as e:
            return
