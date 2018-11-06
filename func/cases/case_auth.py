
async def run_tests(test_session):
    await test_failed(test_session)


# @http_proxy_decorator
# async def test_failed(http_proxy, test_session):
async def test_failed(test_session):
    assert True
    # meta code
    # REQ.AUTH(method:POST, uri: /api/v1/auth, timeout: 5s,)
    # auth_response = http_proxy.fire(request=REQ.AUTH, expected_status=200)