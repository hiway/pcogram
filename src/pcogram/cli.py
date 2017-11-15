#!/usr/bin/env python
import json
import os
import sys
import traceback

from . import TOKENS_PATH, DEFAULT_API_ENDPOINT
from .api import PcogramAPI



class colored(object):
    red = lambda text: '\033[31m{}\033[0m'.format(text)
    green = lambda text: '\033[32m{}\033[0m'.format(text)
    orange = lambda text: '\033[33m{}\033[0m'.format(text)
    blue = lambda text: '\033[34m{}\033[0m'.format(text)
    bold = lambda text: '\033[1m{}\033[0m'.format(text)
    underline = lambda text: '\033[4m{}\033[0m'.format(text)
    reset = '\033[0m'


def auto_install(package):
    import pip, time
    print(colored.orange('Attempting to auto-install required library: {}'.format(package)))
    try:
        time.sleep(1)
        print(colored.bold('Press Ctrl+C to abort.'))
        time.sleep(5)
        pip.main(['install', package])
        print(colored.green('\n\nAuto-installed {!r}, continuing.\n'.format(package)))
        time.sleep(0.3)
    except KeyboardInterrupt:
        print(colored.red('\n\n!! Run "pip install {}" or install {!r} manually.'.format(package, package)))
        sys.exit(-2)
    except Exception as e:
        traceback.print_exc()
        print(colored.red('\n\n!! Run "pip install {}" or install {!r} manually.'.format(package, package)))
        sys.exit(-2)


try:
    import requests
except ImportError:
    try:
        auto_install('requests')
        import requests
    except Exception:
        traceback.print_exc()
        print('ImportError: run "pip install requests"')
        sys.exit(-1)
try:
    import click
except ImportError:
    try:
        auto_install('click')
        import click
    except Exception:
        traceback.print_exc()
        print('ImportError: run "pip install requests"')
        sys.exit(-1)


def load_config(file_name=TOKENS_PATH):
    try:
        with open(file_name, 'r') as infile:
            return json.loads(infile.read())
    except OSError:
        config = {}
        click.echo(colored.blue('Creating tokens file at: {}'.format(file_name)))
        save_config(config, file_name)
        return config


def save_config(config, file_name=TOKENS_PATH):
    if os.path.exists(file_name):
        os.chmod(file_name, 700)
    with open(file_name, 'w') as outfile:
        outfile.write(json.dumps(config or {}))
    os.chmod(file_name, 500)


def load_token(username, file_name=TOKENS_PATH):
    config = load_config(file_name)
    return config[username]


def save_token(username, token, file_name=TOKENS_PATH):
    config = load_config(file_name)
    config[username] = token
    save_config(config)


def require_login(f):
    def wrapper(*args, **kwargs):
        if not os.path.exists(TOKENS_PATH):
            click.echo(colored.red('Please register / login first.'))
            raise click.Abort()
        return f(*args, **kwargs)

    return wrapper


def abort_if_error(response):
    if 'error' in response:
        click.echo(colored.red(response['message']))
        raise click.Abort()


def echo_posts(username, posts):
    click.echo('@{}\t{}'.format(username, '\t'.join([p for p in posts])))


def get_api(account='default', endpoint=DEFAULT_API_ENDPOINT):
    t = load_token(account)
    return PcogramAPI(username=t['username'], token=t['token'], endpoint=endpoint)


@click.group()
def cli():
    pass


@cli.command('register')
def cli_register():
    api = PcogramAPI()
    email = click.prompt('Email')
    username = click.prompt('Username')
    password = click.prompt('Password', hide_input=True)
    response = api.register(username, password, email)
    abort_if_error(response)
    click.echo(response['message'])


@cli.command('login')
@click.option('--default/--no-default', is_flag=True, default=True)
def cli_login(default):
    api = PcogramAPI()
    username = click.prompt('Username')
    password = click.prompt('Password', hide_input=True)
    response = api.login(username, password)
    abort_if_error(response)
    save_token(username, response['data'])
    if default or not os.path.exists(TOKENS_PATH):
        save_token('default', response['data'])
    click.echo(response['message'])


@cli.command('logout')
@click.option('-a', 'account', default='default')
@require_login
def cli_logout(account):
    api = get_api(account)
    response = api.logout()
    abort_if_error(response)
    if click.prompt('Remove {}?'.format(TOKENS_PATH)):
        os.remove(TOKENS_PATH)
    click.echo(response['message'])


@cli.command('post')
@click.argument('message')
@click.option('-a', 'account', default='default')
@require_login
def cli_post(message, account):
    api = get_api(account)
    response = api.post(message)
    abort_if_error(response)
    click.echo(response['message'])


@cli.command('read')
@click.argument('username', default='me')
@click.option('-a', 'account', default='default')
@require_login
def cli_posts(username, account):
    api = get_api(account)
    if username == 'me':
        response = api.posts_by_me()
    else:
        response = api.posts_by_user(username)
    abort_if_error(response)
    echo_posts(response['data']['username'], response['data']['posts'])


@cli.command('follow')
@click.argument('username')
@click.option('-a', 'account', default='default')
@require_login
def cli_follow(username, account):
    api = get_api(account)
    response = api.follow(username)
    abort_if_error(response)
    click.echo(response['message'])


@cli.command('unfollow')
@click.argument('username')
@click.option('-a', 'account', default='default')
@require_login
def cli_unfollow(username, account):
    api = get_api(account)
    response = api.unfollow(username)
    abort_if_error(response)
    click.echo(response['message'])


@cli.command('followers')
@click.option('-a', 'account', default='default')
@require_login
def cli_followers(account):
    api = get_api(account)
    response = api.followers()
    abort_if_error(response)
    click.echo(response['data']['followers'])


@cli.command('following')
@click.option('-a', 'account', default='default')
@require_login
def cli_following(account):
    api = get_api(account)
    response = api.following()
    abort_if_error(response)
    click.echo(response['data']['following'])


@cli.command('timeline')
@click.option('-a', 'account', default='default')
@require_login
def cli_timeline(account):
    api = get_api(account)
    response = api.timeline()
    abort_if_error(response)
    for user_posts in response['data']['timeline']:
        echo_posts(user_posts['username'], user_posts['posts'])


if __name__ == '__main__':
    cli()
