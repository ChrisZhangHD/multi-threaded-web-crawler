# (score, url, left_visited_set, all_site_count)
import time
from urllib.parse import urlparse


class Page:
    def __init__(self, visited_links_count, point_count, parent_depth, page_link):
        # self.parent_links = set()
        self.page_link = page_link
        self.domain = urlparse(self.page_link).netloc
        self.visited_links_count = visited_links_count
        self.point_count = point_count
        self.score = 0
        self.update_score()
        self.download_time = time.asctime(time.localtime(time.time()))
        self.depth = parent_depth + 1
        self.size = 0  # undefined

    def __lt__(self, other):
        return self.score - other.score > 0

    # def add_parent_link(self, parent_link):
    #     self.parent_links.add(parent_link)

    def add_point_count(self):
        self.point_count += 1
        self.update_score()

    def add_visited_link(self):
        self.visited_links_count += 1
        self.update_score()

    def update_score(self):
        self.score = 1.00 / (self.visited_links_count + 1) + self.point_count / 50


if __name__ == '__main__':
    pass
