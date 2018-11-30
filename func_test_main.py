import argparse
from func.runner import run


def get_input_args():
    default_api_url = 'http://test.multy.io'
    default_ws_url = 'ws://127.0.0.1:6780/socket.io/'

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--url',
        help=f'Defines Multy Backend API endpoint, default [{default_api_url}]',
        type=str,
        default=default_api_url,
    )

    parser.add_argument(
        '-w',
        '--ws',
        help=f'Defines Multi Backend WebSocket endpoint, default [{default_ws_url}]',
        type=str,
        default=default_ws_url,
    )

    parser.add_argument(
        '-mv',
        '--multy_version',
        help=f'Defines expected Multy Backend version, default is None and check is skipped',
        type=str,
        default=None,
    )

    # todo: parse cases list from args

    args = parser.parse_args()

    return {
        'url': args.url or default_api_url,
        'ws': args.ws or default_ws_url,
        'multy_version': args.multy_version,
        'cases': [
            'canary',
            # 'exchanger',
            # 'send_transaction',
            'auth',
            'server_config',
            'donations',
            'wallet',
            # 'airdrop',
        ]
    }


if __name__ == '__main__':
    run(get_input_args())
