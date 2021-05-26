import json
import logging
import requests


logger = logging.getLogger(__name__)


def get_external_request(uri, **kwargs):
    try:
        headers = kwargs.get('headers')
        res = requests.get(
            uri,
            headers=headers,
            params=kwargs,
            timeout=5
        )
        content = json.loads(res.content)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        logger.error(msg=e)
        return {}, None
    if res.status_code // 100 in (4, 5):
        logger.error(msg=f'Request finished with status {res.status_code}. Params = {kwargs}, url = {uri}')
    return content, res.status_code


def post_external_request(uri, **kwargs):
    try:
        headers = kwargs.get('headers')
        res = requests.post(
            uri,
            headers=headers,
            data=json.dumps(kwargs),
            timeout=5
        )
        content = json.loads(res.content if res.content else '{}')
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        logger.error(msg=e)
        return {}, None
    if res.status_code // 100 in (4, 5):
        logger.error(msg=f'Request finished with status {res.status_code}. Payload = {kwargs}, url = {uri}')
    return content, res.status_code
