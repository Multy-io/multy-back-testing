import asyncio
from services.eth_node_mock.core import App


def run():
    app = App()
    loop = asyncio.get_event_loop()

    try:
        asyncio.ensure_future(app.start(loop))
        print('node started')
        loop.run_forever()
    except (KeyboardInterrupt,):
        print('lets exit...')
        loop.run_until_complete(app.stop())
        loop.close()

if __name__ == '__main__':
    run()