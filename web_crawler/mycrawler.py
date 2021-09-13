import collections
import heapq
from collections import defaultdict

import crawlerthread
import page
import requestdata


class MyCrawler:

    def __init__(self, result_num):
        self.result_num = result_num
        self.result = []
        self.seeds = None
        self.pq = []
        self.visited_page_link_map = defaultdict(page.Page)
        self.crawled_page_set = set()
        self.domain_map = defaultdict(list)
        self.thread_task = collections.deque()

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
                self.result_num -= 1

    def finish_task(self, future):
        task_result = future.result()
        if not task_result:
            return
        next_url_set, cur_page, result_sentence = task_result
        self.result.append(result_sentence)
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


if __name__ == '__main__':
    query = "nyu tandon computer science"

    my_crawler = MyCrawler(100)
    my_crawler.init_seeds(query)

    my_crawler.put_seeds_to_pq()

    my_crawler.process_pq()

    # print(my_crawler.result)
