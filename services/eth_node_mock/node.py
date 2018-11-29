import asyncio
from aiohttp import web
import json
import websockets
from websockets.exceptions import ConnectionClosed
from services.eth_node_mock.structs import ETH_ROOT_TRANSACTION
from common.utils import get_random_hex


TRANSACTIONS_POOL = dict()


class EthServer:
    def __init__(self):
        self.clients = list()

    def add_client(self, client):
        self.clients.append(client)


class EthWebsocketServer:
    def __init__(self, host, port):
        assert host and port
        self.host, self.port = host, port
        self.clients = set()
        self.ws_handler_future = None
        self.subscription_id = get_random_hex(34)

    async def start_server(self, loop):
        self.ws_handler_future = asyncio.ensure_future(
            websockets.serve(self.handle_connection, '127.0.0.1', 8545))

        # asyncio.gather(self.recurrent_broadcast())

    async def recurrent_broadcast(self):
        try:
            await self.broadcast({
                "jsonrpc": "2.0",
                "method": "eth_subscription",
                "params": {
                    "subscription": self.subscription_id,
                    "result": {
                        "hash": "tmp-test-hash",
                        "difficulty": "0xd9263f42a87",
                        "uncles": [
                            "0x80aacd1ea4c9da32efd8c2cc9ab38f8f70578fcd46a1a4ed73f82f3e0957f936"
                        ],
                    }
                }},
                sleep_timedelta=10,
            )
        except BaseException as err:
            self.log(str(err))

    async def stop_server(self):
        self.ws_handler_future.cancel()

    async def handle_connection(self, websocket, path):
        try:
            self.clients.add(websocket)
            self.log('new client connected')

            async for message in websocket:
                decoded_message = json.loads(message)
                self.log('new message received')
                self.log(message)

                reply_dict = {
                    'jsonrpc': '2.0',
                    'id': decoded_message['id'],
                    'result': '0xcd0c3e8af590364c09d0fa6a1210faf5',
                }
                await websocket.send(json.dumps(reply_dict))
                self.log(f"replied to client {id(websocket)}")
                self.log(reply_dict)

                # mock new transaction from subscription
                if decoded_message['code'] == 1:
                    reply_dict = {
                        'jsonrpc': '2.0',
                        "method": "newPendingTransactions",
                        "params": {
                            "subscription": self.subscription_id,
                            "result": decoded_message['hash']
                        }
                    }

                    TRANSACTIONS_POOL[{decoded_message['hash']] = decoded_message['address']

                    await websocket.send(json.dumps(reply_dict))
                else:
                    self.log("no such code")

        except ConnectionClosed:
            self.log(f"client closed connection {id(websocket)}")
            self.clients.remove(websocket)

    async def broadcast(self, json_message, sleep_timedelta=0):
        if sleep_timedelta > 0:
            await asyncio.sleep(sleep_timedelta)

        for client in self.clients:
            await client.send(json.dumps(json_message))
            self.log(f"broadcast message to client {id(client)}")
            self.log(json_message)

    def log(self, message):
        print(f"eth >> {message}")


async def http_request_handler(request):
    if request.can_read_body:
        request_data = await request.json()
        print('http >> ', request_data)
        assert 'method' in request_data
        assert 'id' in request_data

        if request_data['method'] == 'eth_newPendingTransactionFilter':
            response_data = "0x1"
        elif request_data['method'] == 'eth_getBlockByHash':
            block_hash, is_transaction_full = request_data['params']

            response_data = ETH_ROOT_TRANSACTION
            response_data['block_hash'] = block_hash
        elif request_data['method'] == 'txpool_content':
            response_data = {
                "category": 10,
                "hashTX": "default_hashTX",
                "pending": {},
            }
        elif request_data['method'] == 'eth_sendRawTransaction':
            # 65 is standard length of eth transaction
            response_data = get_random_hex(65)
        elif request_data['method'] == 'eth_getTransactionByHash':
            mydict = TRANSACTIONS_POOL['key']
            del TRANSACTIONS_POOL['key']
            # TODO: resp tx
            # {
            #     "jsonrpc": "2.0",
            #     "id": 1,
            #     "result": {
            #         "blockHash": "0x1d59ff54b1eb26b013ce3cb5fc9dab3705b415a67127a003c3e61eb445bb8df2",
            #         "blockNumber": "0x5daf3b", // 6139707
            #         "from": "0xa7d9ddbe1f17865597fbd27ec712455208b6b76d",
            #         "gas": "0xc350", // 50000
            #         "gasPrice": "0x4a817c800", // 20000000000
            #         "hash": "0x88df016429689c079f3b2f6ad39fa052532c56795b733da78a91ebe6a713944b",
            #         "input": "0x0",
            #         "nonce": "0x15", // 21
            #         "to": "0xf02c1c8e6114b1dbe8937a39260b5b0a374432bb",
            #         "transactionIndex": "0x41", // 65
            #         "value": "0xf3dbb76162000", // 4290000000000000
            #         "v": "0x25", // 37
            #         "r": "0x1b5e176d927f8e9ab405058b2d2457392da3e20f328b16ddabcebc33eaac5fea",
            #         "s": "0x4ba69724e8f69de52f0125ad8b3c5c2cef33019bac3249e2c0a2192766d1721c"
            #     }
            # }
            response_data = get_random_hex(65)

    response = {
        "id": request_data['id'],
        "jsonrpc": "2.0",
        "result": response_data,
    }

    print('http <<', response)

    return web.Response(
        content_type='application/json',
        body=json.dumps(response)
    )
