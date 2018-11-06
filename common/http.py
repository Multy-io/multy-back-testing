import aiohttp


class HttpProxy:
    async def fire(self, req, expected_status=200):
        assert isinstance(req, AbstractHttpRequest)
        # async with aiohttp.ClientSession(read_timeout=HTTP_CALLS_TIMEOUT) as http_session:


class AbstractHttpRequest:
    DEFAULT_HTTP_TIMEOUT = 5

    def get_method(self):
        assert self.method and self.method.lower() in ['get', 'post', 'delete', 'put']
        return self.method

    def get_url(self):
        assert self.api_url
        assert self.uri
        return f'{self.api_url}/{self.uri}'

    def get_timeout(self):
        self.timeout = self.timeout or self.DEFAULT_HTTP_TIMEOUT
        return self.timeout
