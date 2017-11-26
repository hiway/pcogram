#!/usr/bin/env PYTHONIOENCODING=UTF-8 python3
# coding: utf-8
# <bitbar.title>Pcogram</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Harshad Sharma</bitbar.author>
# <bitbar.author.github>hiway</bitbar.author.github>
# <bitbar.desc>Access your Pcogram account.</bitbar.desc>
# <bitbar.dependencies>pcogram,python3.6</bitbar.dependencies>

# IMPORTANT: Replace `python3` in the top line
# with output from `which python` inside your virtualenv
# (where you have run `pip install pcogram` and `pcogram login` before).

from pcogram.api import PcogramAPI
from pcogram.cli import load_token

config = load_token(username='default')
USERNAME = config['username']
TOKEN = config['token']
try:
    api = PcogramAPI(USERNAME, TOKEN)
    response = api.timeline()
    print(response)
    me = {}
    others = []
    for tl in response['data']['timeline']:
        if tl['username'] == USERNAME:
            me = tl
        else:
            others.append(tl)
    print('  '.join(me['posts'][:5]))
    print('---')
    print('post on pcogram| href={}'.format('https://pcogram.com/post'))
    print('---')
    for tl in others[:15]:
        if not tl["posts"]:
            continue
        posts = '  '.join(tl["posts"][:10])
        print(f'@{tl["username"]}| href=https://pcogram.com/{tl["username"]}')
        print(f'{tl["last_posted_at"]}')
        print(f'{posts}')
        print('---')

except Exception as e:
    print('!pcogram | color=red')
    import traceback

    traceback.print_exc()
