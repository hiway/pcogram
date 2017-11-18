import requests
from . import DEFAULT_API_ENDPOINT


class PcogramAPI(object):
    def __init__(self, username='', token='', endpoint=DEFAULT_API_ENDPOINT):
        self.endpoint = endpoint
        self.username = username
        self.token = token

    def get_url(self, path):
        return self.endpoint + path

    def set_token(self, username, token):
        self.username = username
        self.token = token

    def api_call(self, method, path, headers=None, **data):
        headers = headers or {}
        method_handler = getattr(requests, method.lower())
        if self.token:
            headers.update({'Authorization': 'Bearer {}'.format(self.token)})
        r = method_handler(self.get_url(path), json=data, headers=headers)
        return r.json()

    def register(self, username: str, password: str, email: str):
        return self.api_call('post', '/register',
                             username=username,
                             password=password,
                             email=email)

    def login(self, username: str, password: str):
        response = self.api_call('post', '/login',
                                 username=username,
                                 password=password)
        # if 'data' in response:
        #     self.set_token(username, response['data']['token'])
        return response

    def logout(self):
        return self.api_call('post', '/logout')

    def post(self, message: str):
        return self.api_call('post', '/post',
                             message=message)

    def posts_by_me(self):
        return self.api_call('get', '/posts_by_me')

    def posts_by_user(self, username: str):
        return self.api_call('get', '/posts_by_user',
                             username=username)

    def follow(self, username: str):
        return self.api_call('post', '/follow',
                             username=username)

    def unfollow(self, username: str):
        return self.api_call('post', '/unfollow',
                             username=username)

    def followers(self):
        return self.api_call('get', '/followers')

    def following(self):
        return self.api_call('get', '/following')

    def timeline(self):
        return self.api_call('get', '/timeline')
