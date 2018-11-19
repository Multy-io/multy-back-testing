import random
import string
from common.http import BaseHttpRequest
from common import consts


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


# type WalletParams struct {
# 	CurrencyID   int            `json:"currencyID"`
# 	NetworkID    int            `json:"networkID"`
# 	Address      string         `json:"address"`
# 	AddressIndex int            `json:"addressIndex"`
# 	WalletIndex  int            `json:"walletIndex"`
# 	WalletName   string         `json:"walletName"`
# 	IsImported   bool           `json:"isImported"`
# 	Multisig     MultisigWallet `json:"multisig"`
# }
#
# type MultisigWallet struct {
# 	IsMultisig         bool   `json:"isMultisig"`
# 	SignaturesRequired int    `json:"signaturesRequired"`
# 	OwnersCount        int    `json:"ownersCount"`
# 	InviteCode         string `json:"inviteCode"`
# 	IsImported         bool   `json:"isImported"`
# 	ContractAddress    string `json:"contractAddress"`
# }
