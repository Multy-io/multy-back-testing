import random
import string
from common.http import BaseHttpRequest


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
