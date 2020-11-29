import time
import random
from const import *
from util.logger import logger

class Session():
    def __init__(self):
        # requests.adapters.DEFAULT_RETRIES = 5  # 增加重試次數，避免連線失效
        self.has_login = False
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': make_ua(),
            'Accept-Charset': 'utf-8;q=0.7,*;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive'
        }
        self.timeout = 20

    def request(self, method, url, data=None,delay=0):
        for i in range(RETRY_CNT):
            try:
                if delay:time.sleep(delay)
                return self.session.request(
                    method,
                    url,
                    allow_redirects=False,
                    data=data,
                    timeout=self.timeout)
            except (requests.HTTPError, requests.Timeout,requests.ConnectionError) as e:
                logger.warning('Warning: {0}, retrying({1}) ...'.format(str(e), i))
                pass
        logger.error("can't get res: "+url)
        return None


def make_ua():
    rrange = lambda a, b, c=1: c == 1 and random.randrange(a, b) or int(1.0 * random.randrange(a * c, b * c) / c)
    ua = 'Mozilla/%d.0 (Windows NT %d.%d) AppleWebKit/%d (KHTML, like Gecko) Chrome/%d.%d Safari/%d' % (
        rrange(4, 7, 10), rrange(5, 7), rrange(0, 3), rrange(535, 538, 10),
        rrange(21, 27, 10), rrange(0, 9999, 10), rrange(535, 538, 10)
    )
