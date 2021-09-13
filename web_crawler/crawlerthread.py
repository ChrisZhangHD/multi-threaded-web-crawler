from concurrent.futures import ThreadPoolExecutor

from web_crawler import requestdata, htmlparser


class CrawlerThread:

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=10)

    def submit_task(self, cur_page):
        return self.executor.submit(self.put_url_to_pq_task, cur_page)

    def put_url_to_pq_task(self, cur_page):
        cur_link = cur_page.page_link
        cur_html_data = requestdata.get_data_from_request(cur_link)
        if not cur_html_data:
            return
        cur_page_size = str(len(cur_html_data)) + "Bytes"
        result_sentence = str(cur_page.download_time) + " " + cur_link + " " + str(
            cur_page.score) + " " + cur_page_size + " " + str(cur_page.depth)
        print(result_sentence)
        parser = htmlparser.MyHTMLParser(cur_link)
        parser.feed(cur_html_data)
        return [parser.url_set, cur_page, result_sentence]
