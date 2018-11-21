import asyncio
import traceback
from func.cases import cases
from common.utils import TestSession
from common.logger import logger
from common.http import BaseHttpRequest


def run(input_args):
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run_task(input_args))
    except KeyboardInterrupt:
        logger.info('terminate tests launch')
    finally:
        logger.info('close event loop')
        loop.close()

async def run_task(input_args):
    BaseHttpRequest.base_url = input_args['url']
    test_session = TestSession()

    for case_name in input_args.get('cases', []):
        test_session.logger.info(f'start test case [{case_name}]')
        if case_name in cases:  # and is callable
            try:
                await cases[case_name].run_tests(test_session=test_session)
                test_session.inc_assertions_success()
            except AssertionError:
                test_session.inc_assertions_failed()
                test_session.logger.error(f'assertion failed in [{case_name}] case with message [{traceback.format_exc()}]')
            except BaseException:
                test_session.inc_assertions_failed()
                test_session.logger.fatal(f'unexpected error in [{case_name}] case with message [{traceback.format_exc()}]')

    if test_session.is_passed():
        test_session.logger.info(f'PASSED, {test_session.assertions_success} total assertions')
    else:
        test_session.logger.error(
            f'FAILED, {test_session.assertions_success} success assertions and {test_session.assertions_failed} failed'
        )
