from common.http_helper import HttpProxy, create_request
from func.http_requests import REQ


async def run_tests(test_session):
    await test_server_config(test_session)


async def test_server_config(test_session):
    auth_response = await HttpProxy.fire(
        create_request(REQ.AUTH),
        expected_status=200,
    )

    test_session.save_user_context(auth_token=auth_response['token'])
    response = await HttpProxy.fire(
        create_request(REQ.SERVER_CONFIG),
        expected_status=200,
        test_session=test_session
    )

    assert_backend_version = test_session.session_input_args.get('multy_version', None)
    if assert_backend_version:
        assert response['api'] == assert_backend_version, f'Failed server version assertion, got {response["api"]}, ' \
                                                          f'expected {assert_backend_version}'
