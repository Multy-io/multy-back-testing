import time
import uuid
from common.logger import logger


HTTP_CALLS_TIMEOUT = 5  # in seconds


class TestSession:
    """
    todo: isolate test_session and user_context
    withing single test case we can emulate multiple client connections
    which is not really possible(flexible) with one<to>one test_session and user_context rel
    """
    assertions_success = assertions_failed = 0
    cases_failed = cases_success = 0

    def __init__(self):
        self.logger = logger
        # {auth_token: }
        self.user_context = {}

    @property
    def assertions_total(self):
        return self.assertions_error + self.assertions_success

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