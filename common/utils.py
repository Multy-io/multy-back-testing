import functools
import aiohttp
from common.logger import logger


HTTP_CALLS_TIMEOUT = 5  # in seconds


class TestSession:
    assertions_success = assertions_failed = 0
    cases_failed = cases_success = 0

    def __init__(self):
        self.logger = logger

    @property
    def assertions_total(self):
        return self.assertions_error + self.assertions_success

    def inc_assertions_success(self):
        self.assertions_success += 1

    def inc_assertions_failed(self):
        self.assertions_failed += 1

    def is_passed(self):
        return self.assertions_failed == 0


# def http_proxy_decorator(func):
#     @functools.wraps(func)
#     async def wrapped(*args, **kwargs):
#         async with aiohttp.ClientSession(read_timeout=HTTP_CALLS_TIMEOUT) as http_session:
#             await func(http_session, *args, **kwargs)
#
#     return wrapped



