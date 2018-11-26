import asyncio
from copy import copy
from common.realtime import IOPacket, SocketIOConnection
from common.http_helper import HttpProxy, create_request
from common.utils import get_random_string
from func.http_requests import REQ


# todo: move to configuration
URL = 'ws://127.0.0.1:6780/socket.io/'


async def run_tests(test_session):
    await test_airdrop(test_session)


async def test_airdrop(test_session):
    # prepare 1 auth session with created wallet
    u1_auth_request = create_request(REQ.AUTH)
    u1_auth_request.body['userID'] = u1_user_id = get_random_string()
    u1_auth_request.body['deviceID'] = u1_device_id = get_random_string()
    auth_response = await HttpProxy.fire(
        u1_auth_request,
        expected_status=200,
    )

    test_session.save_user_context(auth_token=auth_response['token'])
    create_wallet_request = create_request(REQ.WALLET_CREATE)
    receiver1_wallet_address = get_random_string()
    create_wallet_request.body['address'] = receiver1_wallet_address

    await HttpProxy.fire(create_wallet_request, expected_status=201, test_session=test_session)

    receiver1_id, receiver2_id = u1_user_id, 'rec2'
    receiver1 = SocketIOConnection(URL)
    receiver2 = SocketIOConnection(URL)
    sender1 = SocketIOConnection(URL)

    receiver1.update_dummy_user_headers(userID=receiver1_id)
    receiver2.update_dummy_user_headers(userID=receiver2_id)

    await receiver1.establish_connection()
    await receiver2.establish_connection()
    await sender1.establish_connection()

    await receiver1.send(IOPacket(_type=IOPacket.TYPE_STARTUP_RECEIVER_IS_ON, data={
        'userid': receiver1_id,
        'usercode': receiver1_id,
    }))
    await receiver2.send(IOPacket(_type=IOPacket.TYPE_STARTUP_RECEIVER_IS_ON, data={
        'userid': receiver2_id,
        'usercode': receiver2_id,
    }))

    await asyncio.sleep(1)

    await sender1.send(IOPacket(_type=IOPacket.TYPE_STARTUP_RECEIVERS_AVAILABLE, data={
        'ids': [receiver1_id]
    }))
    io_packet_response = await sender1.recv()
    assert len(io_packet_response.data) == 1, 'invalid available receivers amount'
    assert io_packet_response.data[0]['userid'] == u1_user_id, 'receiver id miss match'
    supported_addrs = io_packet_response.data[0]['supportedAddresses']
    assert len(supported_addrs) > 0
    assert supported_addrs[0]['address'] == receiver1_wallet_address, 'wallet address miss match for receiver1'
