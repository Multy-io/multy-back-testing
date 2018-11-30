import asyncio
import argparse
from services.eth_node_mock.core import App


def get_input_args():
    default_api_url = '127.0.0.1:18545'
    default_ws_url = '127.0.0.1:8545'

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--url',
        help=f'Defines Node server RPC address, default [{default_api_url}]',
        type=str,
        default=default_api_url,
    )

    parser.add_argument(
        '-w',
        '--ws',
        help=f'Defines Node server WebSocket address, default [{default_ws_url}]',
        type=str,
        default=default_ws_url,
    )

    args = parser.parse_args()

    return {
        'url': args.url or default_api_url,
        'ws': args.ws or default_ws_url,
    }

def run(input_args):
    app = App()
    loop = asyncio.get_event_loop()

    try:
        asyncio.ensure_future(app.start(input_args, loop))
        print('node started')
        loop.run_forever()
    except (KeyboardInterrupt,):
        print('lets exit...')
        loop.run_until_complete(app.stop())
        loop.close()

if __name__ == '__main__':
    run(get_input_args())