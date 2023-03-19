from panther.db.connection import RedisConnection
from panther.logger import logger
from panther.middlewares.base import BaseMiddleware
from panther.request import Request
from panther.response import Response


class Middleware(BaseMiddleware):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.validate_host()
        self.validate_port()

    def validate_host(self):
        if host := self.kwargs.get('host'):
            if False:  # TODO: should be valid ip or domain
                logger.critical('Redis "host" is not valid.')
        else:
            self.kwargs['host'] = '127.0.0.1'

    def validate_port(self):
        if port := self.kwargs.get('port'):
            if isinstance(port, str):
                try:
                    self.kwargs['port'] = int(port)
                except ValueError:
                    logger.critical('Redis "port" should be number')

            elif not isinstance(port, int):
                logger.critical('Redis "port" is not valid.')
        else:
            self.kwargs['port'] = 6379

    async def before(self, request: Request) -> Request:
        self.redis = RedisConnection(**self.kwargs)
        return request

    async def after(self, response: Response) -> Response:
        self.redis.close()
        return response
