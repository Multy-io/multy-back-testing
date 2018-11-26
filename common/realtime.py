import aiohttp
import asyncio
from socketIO_client import parsers
from common.utils import get_random_string


class IOPacket:
    TYPE_STARTUP_RECEIVERS_AVAILABLE = 'event:startup:receiver:available'
    TYPE_STARTUP_RECEIVER_IS_ON = 'event:startup:receiver:on'

    def __str__(self):
        return f"<IOPacket type={self.get_type()}, data={self.get_data()}>"

    def __init__(self, _type, data=None):
        self._type, self.data = _type, data

    def get_type(self):
        return self._type

    def get_data(self):
        return self.data


class SocketIOConnection:

    def __init__(self, url):
        self.url = url
        self.ws_connection = None
        self.dummy_user_headers = {
            'userID': get_random_string(),
            'deviceType': get_random_string(),
            'jwtToken': get_random_string(),

        }

    def update_dummy_user_headers(self, **kwargs):
        self.dummy_user_headers.update(kwargs)

    async def establish_connection(self):
        self.ws_connection = await aiohttp.ClientSession().ws_connect(self.url, headers=self.dummy_user_headers)

    async def send(self, io_packet):
        assert isinstance(io_packet, IOPacket)
        encoded_packet = parsers.format_socketIO_packet_data(
            ack_id=42,  # magic number, ack
            args=[io_packet.get_type(), io_packet.get_data()]
        )
        await self.ws_connection.send_str(encoded_packet)

    async def recv(self):
        """
        todo: refactor websocket messages receiving to callback-based way (or queue)
        for now it's tricky but works
        """
        packet = None
        while True:
            msg = await self.ws_connection.receive()

            parsed_packet = parsers.parse_socketIO_packet_data(msg.data.encode())
            if not parsed_packet.args or not isinstance(parsed_packet.args, list):
                continue

            packet_type, packet_data = parsed_packet.args
            if 'exchange' in packet_type:
                continue

            packet = IOPacket(packet_type, packet_data)
            break

        return packet
