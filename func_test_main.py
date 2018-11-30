import argparse
from func.runner import run


def get_input_args():
    default_api_url = 'http://127.0.0.1:6778'
    default_ws_url = 'ws://127.0.0.1:6780/socket.io/'

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--url',
        help=f'Defines Multy Backend API endpoint, default [{default_api_url}]',
        type=str,
    )

    parser.add_argument(
        '-w',
        '--ws',
        help=f'Defaines Multi Backend WebSocket endpoint, default [{default_ws_url}]',
        type=str,
    )

    # todo: parse cases list from args

    args = parser.parse_args()

    return {
        'url': args.url or default_api_url,
        'ws': args.ws or default_ws_url,
        'cases': [
            'canary',
            # 'exchanger',
            # 'send_transaction',
            # 'auth',
            # 'server_config',
            # 'donations',
            # 'wallet',
            'airdrop',
        ]
    }


if __name__ == '__main__':
    run(get_input_args())
