import asyncio
from aiohttp import web
import json
import websockets


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

    async def stop_server(self):
        self.ws_handler_future.cancel()

    async def handle_connection(self, websocket, path):
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

    async def broadcast(self, json_message):
        for client in self.clients:
            await client.send(json.dumps(json_message))
            self.log(f"broadcast message to client {id(client)}")
            self.log(json_message)


    def log(self, message):
        print(f"eth >> {message}")


async def http_request_handler(request):
    if request.can_read_body:
        request_data = await request.json()
        print('request (json) >> ', request_data)
    else:
        print('empty request body')

    return web.Response(
        content_type='application/json',
        body=json.dumps({
            "id": 1,
            "jsonrpc": "2.0",
            "result": json.dumps({
                "admin": "1.0",
                "db": "1.0",
                "debug": "1.0",
                "eth": "1.0",
                "miner": "1.0",
                "net": "1.0",
                "personal": "1.0",
                "shh": "1.0",
                "txpool": "1.0",
                "web3": "1.0"
            })
        })
    )
