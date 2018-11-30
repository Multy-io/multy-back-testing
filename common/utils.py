import time
import uuid
from common.logger import logger
import random


HTTP_CALLS_TIMEOUT = 5  # in seconds


class TestSession:
    """
    TODO: isolate test_session and user_context
    withing single test case we can emulate multiple client connections
    which is not really possible(flexible) with one<to>one test_session and user_context rel
    """
    assertions_success = assertions_failed = 0
    cases_failed = cases_success = 0

    def __init__(self, session_input_args=None):
        self.logger = logger
        # {auth_token: }
        self.user_context = {}
        self.session_input_args = session_input_args or {}

    @property
    def assertions_total(self):
        return self.assertions_failed + self.assertions_success

    def inc_assertions_success(self):
        self.assertions_success += 1

    def inc_assertions_failed(self):
        self.assertions_failed += 1

    def is_passed(self):
        return self.assertions_failed == 0

    def save_user_context(self, **kwargs):
        self.user_context = kwargs
        return self


def get_random_string():
    return f"{time.time()}_{uuid.uuid4().hex[0:10]}"


def get_random_hex(size=1):
    result = []

    if size > 3:
        size -= 3

    result.append("0x")
    result.append(str(random.choice("0123456789ABCDEF")))

    for i in range(size):
        result.append(str(random.choice("0123456789ABCDEF")))
    return "".join(result).lower()
