import singer
import backoff
import datetime

from tap_kit import BaseClient

LOGGER = singer.get_logger()


class RateLimitException(Exception):
    pass


class ABCClient(BaseClient):
    @backoff.on_exception(backoff.expo,
                          RateLimitException,
                          max_tries=5,
                          factor=3)
    def make_request(self, request_config, body=None, method='GET'):
        LOGGER.info(f"Making request at {datetime.now()}")
        LOGGER.info("Making {} request to {}".format(
            method, request_config['url']))

        with singer.metrics.Timer('request_duration', {}) as timer:
            response = self.requests_method(method, request_config, body)

        if response.status_code in [429, 500, 503]:
            LOGGER.info(f"[Error {response.status_code}] with this "
                        f"response:\n {response}")
            raise RateLimitException()

        response.raise_for_status()

        return response
