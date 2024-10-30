import requests
import json
from datetime import datetime
from pathlib import Path

class RequestsLogDict(dict):
    @classmethod
    def from_response(cls, resp: requests.Response, _root=True):
        d = {
            'method': resp.request.method,
            'url': resp.request.url,
            'headers': dict(resp.request.headers),
            'response': {
                'status': resp.status_code,
                'headers': dict(resp.headers),
                'content': {
                    'text': resp.text,
                }
            },
        }

        if _root:
            d['history'] = [cls.from_response(h, _root=False) for h in resp.history]
        return d


def log_http_request(response):
    now = datetime.now()
    http_archive = RequestsLogDict.from_response(response)
    filename = Path('.') / 'requests_logs' / f'{now:%Y%m%d-%H%M%S.%f}.dat'
    filename.parents[0].mkdir(parents=True, exist_ok=True)
    with open(filename, 'w') as f_response:
        f_response.write(json.dumps(http_archive, indent=2))
