import json

import requestdata


class Search(object):
    def __init__(self, search_key_words):
        self.key_words = search_key_words
        self.seeds = set()

    def getURLs(self):
        self.key_words = ["nyu", "tandon", "student"]
        api_key = "AIzaSyA7aWYZkb27pfHB4gSDSbvuqeZYzWzEeSk"
        program_search_engine_id = "243c4562e747901f1"
        # default 10 result
        google_api_url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s" \
                         % (api_key, program_search_engine_id, "+".join(self.key_words))
        res = requestdata.get_data_from_request(google_api_url)
        json_data = json.loads(res[0])
        item_list = json_data["items"]
        for item in item_list:
            self.seeds.add(item["link"])
        return self.seeds
        pass


if __name__ == "__main__":
    # contacter = SearchGoogle("Torsten Suel",15)
    # print(contacter.getURLs())
    # to search
    search = Search("nyu tandon")
    search.getURLs()
    print(search.seeds)
