from func.runner import run

# def run():
#     input_args = get_input_args()
#     print(input_args)

def get_input_args():
    return {
        # 'url': 'http://api.multy.io',
        # 'url': 'http://test.multy.io',
        'url': 'http://127.0.0.1:6778',
        'cases': [
            'canary',
            'auth',
        ]
    }


if __name__ == '__main__':
    run(get_input_args())
