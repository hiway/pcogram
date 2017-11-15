import os

TOKENS_PATH = os.path.expanduser('~/.pcogram.tokens')
DEFAULT_API_ENDPOINT = os.getenv('PCOGRAM_API_ENDPOINT', 'https://pcogram.com/api')

from .api import PcogramAPI

__all__ = [
    'PcogramAPI'
]
