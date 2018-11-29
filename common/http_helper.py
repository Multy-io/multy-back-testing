import aiohttp
from aiohttp.connector import TCPConnector
from schema import loader as schema_loader


HTTP_OK = 200
HTTP_CREATED = 201
HTTP_FORBIDDEN = 403
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404


class HttpProxy:

    @classmethod
    def is_session_authenticated(cls, test_session):
        if not test_session:
            return False

        return test_session and 'auth_token' in test_session.user_context

    @classmethod
    def get_session_auth_token(cls, test_session):
        return test_session.user_context['auth_token']

    @classmethod
    async def fire(cls, req, expected_status=HTTP_OK, test_session=None):
        assert isinstance(req, BaseHttpRequest)

        if req.schema_request:
            schema_loader.validate(
                req.body,
                schema_loader.get_schema(req.schema_request)
            )

        client_session_coro = aiohttp.ClientSession(
            read_timeout=req.get_timeout(),
            connector=TCPConnector(verify_ssl=False)
        )
        async with client_session_coro as http_session:
            rest_call = getattr(http_session, req.get_method())
            rest_call_kwargs = dict()
            if req.is_request_body_provided():
                rest_call_kwargs['json'] = req.get_prepared_body()

            if cls.is_session_authenticated(test_session):
                rest_call_kwargs['headers'] = {
                    'Authorization': f"Bearer {cls.get_session_auth_token(test_session)}"
                }

            async with rest_call(req.get_url(), **rest_call_kwargs) as response:
                assert expected_status == response.status
                if req.schema_response and response.status in [HTTP_OK, HTTP_CREATED]:
                    schema_loader.validate(
                        response_data,
                        schema_loader.get_schema(req.schema_response)
                    )

                return response_data


class BaseHttpRequest:
    DEFAULT_HTTP_TIMEOUT = 5
    # populates on startup with url from input_args
    base_url = ''
    schema_request = None
    schema_response = None
    body = None

    def get_method(self):
        assert self.method and self.method.lower(
        ) in ['get', 'post', 'delete', 'put']
        return self.method

    def is_request_body_provided(self):
        return bool(self.body) and self.method.lower() in ['post', 'put']

    def get_prepared_body(self):
        return self.body

    def get_url(self):
        assert self.base_url
        assert self.uri
        return f'{self.base_url}{self.uri}'

    def get_timeout(self):
        return getattr(self, 'timeout', self.DEFAULT_HTTP_TIMEOUT)


def create_request(request, body=None):
    assert issubclass(request, BaseHttpRequest)

    instantiated_request = request()
    if body:
        instantiated_request.body = body

    return instantiated_request
