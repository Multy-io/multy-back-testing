from common.http_helper import HttpProxy, create_request
from func.http_requests import REQ


async def run_tests(test_session):
    await test_exchangelly_basic(test_session)


async def test_exchangelly_basic(test_session):
    auth_response = await HttpProxy.fire(
        create_request(REQ.AUTH),
        expected_status=200,
    )

    test_session.save_user_context(auth_token=auth_response['token'])
    await HttpProxy.fire(
        req=create_request(REQ.GET_EXCHANGER_CURRENCIES),
        test_session=test_session,
    )

    await HttpProxy.fire(
        req=create_request(REQ.GET_EXCHANGER_AMOUNT_TO_EXCHANGE),
        test_session=test_session,
    )

    response = await HttpProxy.fire(
        req=create_request(REQ.EXCHANGER_CREATE_TRANSACTION),
        test_session=test_session,
    )

    assert response['payinAddress'] != response['payoutAddress'], 'exchange addresses should not be the same'