#!/usr/bin/env PYTHONIOENCODING=UTF-8 /Users/harshad/.virtualenvs/pcogram_server-P34bbgy0/bin/python
# coding: utf-8
# <bitbar.title>Pcogram</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Harshad Sharma</bitbar.author>
# <bitbar.author.github>hiway</bitbar.author.github>
# <bitbar.desc>Access your Pcogram account.</bitbar.desc>
# <bitbar.dependencies>pcogram,python3.6</bitbar.dependencies>


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
    print(''.join(me['posts'][:5]))
    print('---')
    print('post| href={}'.format('https://pcogram.com/post'))
    print('---')
    for tl in others[:15]:
        if not tl["posts"]:
            continue
        print(f'{tl["username"]}: {tl["posts"][:5]}: {tl["last_posted_at"]}')

except Exception as e:
    print('!pcogram | color=red')
    import traceback

    traceback.print_exc()
