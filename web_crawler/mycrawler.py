import collections
import datetime
import heapq
import logging
from collections import defaultdict

import crawlerthread
import page
import requestdata


class MyCrawler:

    def __init__(self, result_num):
        self.result_num = result_num
        self.seeds = None
        self.pq = []
        self.visited_page_link_map = defaultdict(page.Page)
        self.crawled_page_set = set()
        self.domain_map = defaultdict(list)
        self.thread_task = collections.deque()
        self.robot_map = {}
        self.logger = self.logger_config("log.txt", log_name="crawler result")

    def init_seeds(self, query):
        self.seeds = requestdata.search_from_google(query)

    def put_seeds_to_pq(self):
        for seed in self.seeds:
            new_page = page.Page(0, 0, -1, seed)
            if seed not in self.visited_page_link_map:
                self.visited_page_link_map[seed] = new_page
                heapq.heappush(self.pq, new_page)

    def process_pq(self):
        thread_executor = crawlerthread.CrawlerThread()
        self.thread_task.extend([thread_executor.submit_task(self.visited_page_link_map[seed]) for seed in self.seeds])
        while len(self.thread_task) > 0 and self.result_num > 0:
            while self.pq and self.result_num > 0:
                cur_future = self.thread_task.popleft()
                while len(self.thread_task) and not cur_future.done():
                    self.thread_task.append(cur_future)
                    cur_future = self.thread_task.popleft()
                self.finish_task(cur_future)
                heapq.heapify(self.pq)
                cur_page = heapq.heappop(self.pq)
                self.thread_task.append(thread_executor.submit_task(cur_page))

    def finish_task(self, future):
        task_result = future.result()
        if not task_result:
            return
        next_url_set, cur_page, result_sentence = task_result
        self.result_num -= 1
        self.logger.info(result_sentence)
        for next_url in next_url_set:
            if next_url in self.crawled_page_set:
                continue
            if next_url in self.visited_page_link_map:
                # update page importance
                self.visited_page_link_map[next_url].add_point_count()
                # update novelty if they have same domain
                if self.visited_page_link_map[next_url].domain == cur_page.domain:
                    self.visited_page_link_map[next_url].add_visited_link()
            else:
                next_page = page.Page(0, 0, cur_page.depth, next_url)
                self.visited_page_link_map[next_url] = next_page
                heapq.heappush(self.pq, next_page)

    def logger_config(self, log_path, log_name):
        logger = logging.getLogger(log_name)
        logger.setLevel(level=logging.DEBUG)
        handler = logging.FileHandler(log_path, encoding="UTF-8")
        handler.setLevel(level=logging.INFO)
        console = logging.StreamHandler()
        console.setLevel(level=logging.DEBUG)
        logger.addHandler(handler)
        logger.addHandler(console)
        return logger


if __name__ == '__main__':
    startTime = datetime.datetime.now()
    query = "nyu tandon"

    my_crawler = MyCrawler(100)
    my_crawler.init_seeds(query)

    my_crawler.put_seeds_to_pq()

    my_crawler.process_pq()

    endTime = datetime.datetime.now()
    print((endTime - startTime).seconds)
