from common.http_helper import HttpProxy, create_request
from func.http_requests import REQ
from common import consts
from common.utils import get_random_hex
from common import http_helper


async def run_tests(test_session):
    await test_(test_session)


async def test_(test_session):
    auth_response = await HttpProxy.fire(
        create_request(REQ.AUTH),
        expected_status=200,
    )

    test_session.save_user_context(auth_token=auth_response['token'])

    create_wallet_request = create_request(REQ.WALLET_CREATE)
    create_wallet_request.body['address'] = get_random_hex(42)

    await HttpProxy.fire(create_wallet_request, expected_status=201, test_session=test_session)

    get_wallet_response = await HttpProxy.fire(
        create_request(REQ.WALLET_GET),
        expected_status=200,
        test_session=test_session
    )

    # TODO: take last action time of wallet from resp

    create_send_eth_transaction_request = create_request(REQ.SEND_TRANSACTION)
    create_send_eth_transaction_request.body["payload"]["address"] = create_wallet_request.body['address']
    create_send_eth_transaction_request.body["payload"]["transaction"] = get_random_hex(
        84)

    create_send_eth_transaction_request.body["currencyID"] = consts.ETH_CURRENCY_ID_ETH
    create_send_eth_transaction_request.body["networkID"] = consts.ETH_CURRENCY_NETWORK

    send_eth_transaction_response = await HttpProxy.fire(create_send_eth_transaction_request, expected_status=http_helper.HTTP_OK, test_session=test_session)

    # TODO: send req to mock node that will produce new tx with txid and address to ns
    # make another req for wallet verbose and compare last action old and new one
