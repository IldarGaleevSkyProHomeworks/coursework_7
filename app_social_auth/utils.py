import hashlib
import hmac
from collections import OrderedDict
from datetime import datetime

from django.conf import settings


def check_telegram_data(data: dict) -> dict[str, str]:
    data = data.copy()
    source_hash = data.pop('hash')[0]
    ordered_data = OrderedDict(sorted(data.items()))
    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    data_check_string = '\n'.join([f'{key}={value}' for key, value in ordered_data.items()])

    hashed_data = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    if hashed_data != source_hash:
        raise ValueError('Data is not correct')

    curr_timestamp = round(datetime.now().timestamp())
    if curr_timestamp - int(data['auth_date']) > settings.MAX_OAUTH_TIMEOUT:
        raise TimeoutError('Data is outdated')

    return data
