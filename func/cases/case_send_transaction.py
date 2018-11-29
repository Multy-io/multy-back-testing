import json
from common.http_helper import HttpProxy, create_request
from common.utils import get_random_string
from func.http_requests import REQ
from common.utils import get_random_hex
from common import http_helper
from common import consts


async def run_tests(test_session):
    await test_send_transaction(test_session)


async def test_send_transaction(test_session):
    auth_response = await HttpProxy.fire(
        create_request(REQ.AUTH),
        expected_status=200,
    )

    test_session.save_user_context(auth_token=auth_response['token'])

    create_send_eth_transaction_request = create_request(REQ.SEND_TRANSACTION)
    create_send_eth_transaction_request.body["payload"]["address"] = get_random_hex(42)
    create_send_eth_transaction_request.body["payload"]["transaction"] = get_random_hex(84)
    create_send_eth_transaction_request.body["currencyID"] = consts.ETH_CURRENCY_ID_ETH
    create_send_eth_transaction_request.body["networkID"] = consts.ETH_CURRENCY_NETWORK

    await HttpProxy.fire(
        create_send_eth_transaction_request,
        expected_status=http_helper.HTTP_OK,
        test_session=test_session,
    )
