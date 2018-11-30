from aiohttp import web
from services.eth_node_mock.node import EthWebsocketServer, http_request_handler


class App:
    def __init__(self):
        self.eth_node = None
        self.http_server = None

    async def start(self, input_args, loop):
        api_url = input_args['url']
        ws_url = input_args['ws']

        self.eth_node = EthWebsocketServer(*api_url.split(':'))
        await self.eth_node.start_server(loop)

        self.http_server = await loop.create_server(
            web.Server(http_request_handler),
            *ws_url.split(':'),
        )

    async def stop(self):
        await self.eth_node.stop_server()
        self.http_server.close()
