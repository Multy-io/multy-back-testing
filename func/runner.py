from func.cases import cases
from common.utils import TestSession


def run(input_args):

    test_session = TestSession()

    for case_name in input_args.get('cases', []):
        if case_name in cases: # and is callable
            try:
                cases[case_name].run_tests(test_session=test_session)
                test_session.inc_assertions_success()
            except AssertionError as err:
                test_session.inc_assertions_failed()
                test_session.logger.error(f'assertion failed in [{case_name}] case with message [{str(err)}]')
            except BaseException as err:
                test_session.inc_assertions_failed()
                test_session.logger.fatal(f'unexpected error in [{case_name}] case with message [{str(err)}]')

    if test_session.is_passed():
        test_session.logger.info(f'PASSED, {test_session.assertions_success} total assertions')
    else:
        test_session.logger.error(
            f'FAILED, {test_session.assertions_success} success assertions and {test_session.assertions_failed} failed'
        )
