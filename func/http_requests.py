from common.http import BaseHttpRequest


class REQ:

    class AUTH(BaseHttpRequest):
        method = 'post'
        uri = '/auth'
        schema_request = 'multi:HttpAuthRequest'
        schema_response = 'multi:HttpAuthResponse'
