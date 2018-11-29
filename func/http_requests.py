import random
import string
from common.http_helper import BaseHttpRequest
from common import consts
from common.utils import get_random_hex


class REQ:
    class AUTH(BaseHttpRequest):
        method = 'post'
        uri = '/auth'
        schema_request = 'multy:HttpAuthRequest'
        schema_response = 'multy:HttpAuthResponse'

        body = {
            'userID': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)),
            'deviceID': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16)),
            'deviceType': 1,
            'appVersion': '1.1.1',
            'pushToken': 'no'
        }

    class SERVER_CONFIG(BaseHttpRequest):
        method = 'get'
        uri = '/server/config'
        # todo provide schemas

    class DONATIONS(BaseHttpRequest):
        method = 'get'
        uri = '/donations'
        # todo provide schemas

    class WALLET_CREATE(BaseHttpRequest):
        method = 'post'
        uri = '/api/v1/wallet'

        schema_request = 'multy:HttpWalletCreateRequest'
        schema_response = 'multy:HttpWalletCreateResponse'

        body = {
            'currencyID': consts.ETH_CURRENCY_ID_ETH,
            'networkID': consts.ETH_CURRENCY_NETWORK,
            'address': 'address_default',
            'addressIndex': 300,
            'walletIndex': 300,
            'walletName': 'wallet_name_default',
            'isImported': False,
            'multisig': {
                'isMultisig': False,
                'signaturesRequired': 1,
                'ownersCount': 1,
                'inviteCode': 'invite_code_default',
                'isImported': False,
                'contractAddress': 'contract_address_default',
            }
        }

    class WALLET_GET(BaseHttpRequest):
        method = 'get'
        uri = '/api/v1/wallets/verbose'

    class SEND_TRANSACTION(BaseHttpRequest):
        method = 'post'
        uri = '/api/v1/transaction/send'

        schema_request = 'multy:HttpSendETHTransactionRequest'
        schema_response = 'multy:HttpSendETHTransactionResponse'

        body = {
            'currencyID': 0,
            'networkID': 0,
            'payload': {
                'address': '',
                'transaction': '',
                'ishd': False
            }
        }

    class GET_EXCHANGER_CURRENCIES(BaseHttpRequest):
        method = 'get'
        uri = '/api/v1/exchanger/supported_currencies'

        schema_request = None
        schema_response = 'multy:HttpExchangerGetSupportedCurrenciesResponse'

    class GET_EXCHANGER_AMOUNT_TO_EXCHANGE(BaseHttpRequest):
        method = 'post'
        uri = '/api/v1/exchanger/exchange_amount'

        schema_request = 'multy:HttpExchangerGetExchangeAmountRequest'
        schema_response = 'multy:HttpExchangerGetExchangeAmountResponse'

        body = {
            'from': 'btc',
            'to': 'eth',
            'amount': 1.2,
        }

    class EXCHANGER_CREATE_TRANSACTION(BaseHttpRequest):
        method = 'post'
        uri = '/api/v1/exchanger/transaction'

        schema_request = 'multy:HttpExchangerCreateTransactionRequest'
        schema_response = 'multy:HttpExchangerCreateTransactionResponse'

        body = {
            'from': 'btc',
            'to': 'eth',
            'amount': 1.2,
            'address': '0xe6001AEb462B880A202597CAA3ad064093dD4880',
        }