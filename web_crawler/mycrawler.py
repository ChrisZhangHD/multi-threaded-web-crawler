import heapq
from collections import defaultdict
from urllib.parse import urlparse

import requestdata
import page
import htmlparser


class MyCrawler:

    def __init__(self, result_num):
        self.result_num = result_num
        self.result = []
        self.seeds = None
        self.pq = []
        self.visited_page_link_map = defaultdict(page.Page)
        self.crawled_page_set = set()
        self.domain_map = defaultdict(list)

    def init_seeds(self, query):
        self.seeds = requestdata.search_from_google(query)

    def put_seeds_to_pq(self):
        for seed in self.seeds:
            new_page = page.Page(0, 0, -1, seed)
            if seed not in self.visited_page_link_map:
                self.visited_page_link_map[seed] = new_page
                heapq.heappush(self.pq, new_page)

    def process_pq(self):
        while self.pq and self.result_num > 0:
            heapq.heapify(self.pq)
            cur_page = heapq.heappop(self.pq)
            cur_link = cur_page.page_link
            self.crawled_page_set.add(cur_link)
            cur_domain = urlparse(cur_link).netloc
            del self.visited_page_link_map[cur_link]
            request_result = requestdata.get_data_from_request(cur_link)
            if not request_result:
                continue
            cur_html_data, cur_page_size = request_result[0], request_result[1]
            # print(str(cur_page.score) + " " + cur_link)
            self.result.append(cur_link + "  " + str(cur_page.score) + " " + cur_page_size + " " + str(cur_page.depth))
            parser = htmlparser.MyHTMLParser(cur_link)
            parser.feed(cur_html_data)

            for next_url in parser.url_set:
                if next_url in self.crawled_page_set:
                    continue
                if next_url in self.visited_page_link_map:
                    # update page importance
                    self.visited_page_link_map[next_url].add_point_count()
                    # update novelty if they have same domain
                    if self.visited_page_link_map[next_url].domain == cur_domain:
                        self.visited_page_link_map[next_url].add_visited_link()
                else:
                    next_page = page.Page(0, 0, cur_page.depth, next_url)
                    self.visited_page_link_map[next_url] = next_page
                    heapq.heappush(self.pq, next_page)
            self.result_num -= 1


if __name__ == '__main__':
    query = "nyu tandon computer science"

    my_crawler = MyCrawler(25)
    my_crawler.init_seeds(query)

    my_crawler.put_seeds_to_pq()

    my_crawler.process_pq()

    print(my_crawler.result)
