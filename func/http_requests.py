from common.http import AbstractHttpRequest


class REQ:

    class AUTH(AbstractHttpRequest):
        method = 'post'
        uri = '/api/v1/auth'
        schema_request = 'multi:HttpAuthRequest'
        schema_response = 'multi:HttpAuthResponse'
