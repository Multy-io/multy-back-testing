import argparse
from func.runner import run


def get_input_args():
    default_api_url = 'http://127.0.0.1:6778'

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u',
        '--url',
        help=f'Defines Multy Backend API endpoint, default [{default_api_url}]',
        type=str,
    )

    # todo: parse cases list from args

    args = parser.parse_args()

    return {
        'url': args.url or default_api_url,
        'cases': [
            'canary',
            'send_transaction',
            # 'last_action_time_wallet_eth',
            # 'auth',
            # 'server_config',
            # 'donations',
            # 'wallet',
            # 'airdrop',
        ]
    }


if __name__ == '__main__':
    run(get_input_args())
