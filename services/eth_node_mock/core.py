from aiohttp import web
from services.eth_node_mock.node import EthWebsocketServer, http_request_handler


class App:
    def __init__(self):
        self.eth_node = None
        self.http_server = None

    async def start(self, loop):
        self.eth_node = EthWebsocketServer('127.0.0.1', 8545)
        await self.eth_node.start_server(loop)

        self.http_server = await loop.create_server(
            web.Server(http_request_handler),
            *'127.0.0.1:18545'.split(':'),
        )

    async def stop(self):
        await self.eth_node.stop_server()
        self.http_server.close()
