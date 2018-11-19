from datetime import datetime, timezone
from common.http import HttpProxy, create_request
from func.http_requests import REQ


async def run_tests(test_session):
    await test_common_auth(test_session)


async def test_common_auth(test_session):
    auth_request = create_request(REQ.AUTH)
    auth_response = await HttpProxy.fire(
        auth_request,
        200
    )

    token_expires_at = datetime.strptime(auth_response['expire'], '%Y-%m-%dT%H:%M:%S%z')
    assert  token_expires_at > datetime.now(timezone.utc), 'token expiration should be in future'
