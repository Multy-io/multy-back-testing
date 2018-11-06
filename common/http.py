import aiohttp


HTTP_OK = 200
HTTP_FORBIDDEN = 403
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404


class HttpProxy:

    @classmethod
    async def fire(cls, req, expected_status=HTTP_OK):
        assert isinstance(req, BaseHttpRequest)

        async with aiohttp.ClientSession(read_timeout=req.get_timeout()) as http_session:
            rest_call = getattr(http_session, req.get_method())
            rest_call_args = [req.get_url()]
            if req.is_request_body_provided():
                rest_call_args.append(req.get_prepared_body())

            async with rest_call(*rest_call_args) as response:
                response_data = await response.text()

                print(response.status)
                print(response_data)
                assert expected_status == response.status





class BaseHttpRequest:
    DEFAULT_HTTP_TIMEOUT = 5
    # populates on startup with url from input_args
    base_url = ''


    # def __init__(self):
        # static_props = ['method', 'body', 'api_url', 'uri', 'timeout']
        # for prop in static_props:
        #     setattr(self, prop, getattr(BaseHttpRequest))

    def get_method(self):
        assert self.method and self.method.lower() in ['get', 'post', 'delete', 'put']
        return self.method

    def is_request_body_provided(self):
        return bool(self.body) and self.method.lower() in ['post', 'put']

    def set_body(self, body):
        self.body = body
        return self

    def get_prepared_body(self):
        # todo decode or not?
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
    instantiated_request.body = body if body else None

    return instantiated_request
