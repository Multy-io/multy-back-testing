from common.http import HttpProxy, create_request
from common.utils import get_random_string
from func.http_requests import REQ


async def run_tests(test_session):
    await test_wallet_create(test_session)


async def test_wallet_create(test_session):
    auth_response = await HttpProxy.fire(
        create_request(REQ.AUTH),
        expected_status=200,
    )

    test_session.save_user_context(auth_token=auth_response['token'])

    create_wallet_request = create_request(REQ.WALLET_CREATE)
    create_wallet_request.body['address'] = get_random_string()
    
    response_data = await HttpProxy.fire(
        create_wallet_request,
        expected_status=201,
        test_session=test_session
    )

    await HttpProxy.fire(
        create_wallet_request,
        expected_status=400,
        test_session=test_session
    )

    print(response_data)
