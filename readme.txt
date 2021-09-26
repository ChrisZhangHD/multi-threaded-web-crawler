- crawlerthread.py
  multi-thread to deal with the request and parse function.

- htmlparser.py
  deal with the html parser.

- mycrawler.py
  main function and include priority queue operation and call multi-thread.

- page.py
  define the page object and include some basic parameters of page.
  score = point_count / 20 (importance) + 1 / (1 + same_domain_visited) (novelty)

- requestdata.py
  send http request and get data.

How to run my crawler?
python3 mycrawler.py
and then input the keywords. there is no limitation.
finally input the int number of total pages you want to get.