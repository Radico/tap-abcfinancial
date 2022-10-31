import singer
import time
from datetime import datetime

from tap_kit import BaseClient

LOGGER = singer.get_logger()


class ABCClient(BaseClient):
    RETRYING_STATUS_CODES = [429, 500, 503]
    def make_request(self, request_config, body=None, method='GET'):
        retries = 5
        delay = 30
        backoff = 1.5
        attempt = 1
        while retries >= attempt:
            LOGGER.info(f"Making request at {datetime.now()}")
            LOGGER.info("Making {} request to {}".format(
                method, request_config['url']))

            with singer.metrics.Timer('request_duration', {}) as timer:
                response = self.requests_method(method, request_config, body)

        if response.status_code in RETRYING_STATUS_CODES:
            LOGGER.info(f"[Error {response.status_code}] with this "
                        f"response:\n {response}")
            time.sleep(delay)
            delay *= backoff
            attempt += 1
        else:
            return response

        logger.info(f"Reached maximum retries ({retries}), failing...")
        raise ValueError("Maximum retries reached")

