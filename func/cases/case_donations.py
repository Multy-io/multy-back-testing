from common.http import HttpProxy, create_request
from func.http_requests import REQ


async def run_tests(test_session):
    await test_donation(test_session)


async def test_donation(test_session):
    auth_response = await HttpProxy.fire(
        create_request(REQ.AUTH),
        expected_status=200,
    )

    test_session.save_user_context(auth_token=auth_response['token'])
    await HttpProxy.fire(
        create_request(REQ.DONATIONS),
        expected_status=200,
        test_session=test_session
    )
