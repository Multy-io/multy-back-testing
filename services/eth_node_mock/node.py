import asyncio
from aiohttp import web
import json
import websockets
from websockets.exceptions import ConnectionClosed
from services.eth_node_mock.structs import ETH_ROOT_TRANSACTION


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

    async def start_server(self, loop):
        self.ws_handler_future = asyncio.ensure_future(websockets.serve(self.handle_connection, '127.0.0.1', 8545))

        # asyncio.gather(self.recurrent_broadcast())

    async def recurrent_broadcast(self):
        while 1:
            try:
                await self.broadcast({
                    "jsonrpc": "2.0",
                    "method": "eth_subscription",
                    "params": {
                        "subscription": "0xcd0c3e8af590364c09d0fa6a1210faf5",
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

            await asyncio.sleep(3)

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
        except ConnectionClosed:
            self.log(f"client closed connection {id(websocket)}")
            self.clients.remove(websocket)

    async def broadcast(self, json_message, sleep_timedelta = 0):
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
