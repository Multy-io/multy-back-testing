from common.logger import logger


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

