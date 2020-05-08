import click
import configparser
import os
import requests
import time

from rich.console import Console

config = configparser.ConfigParser()
console = Console()


def create_config_file():
    config.add_section('main')
    config['main']['username'] = ''
    config['main']['password'] = ''

    with open('config.ini', 'w') as f:
        config.write(f)


if not os.path.exists('config.ini'):
    create_config_file()
else:
    config.read('config.ini')


@click.command()
@click.option('--username',
              prompt=True)
@click.option('--password',
              prompt=True)
def prompt_username(username, password):
    config['main']['username'] = username
    config['main']['password'] = password
    with open('config.ini', 'w') as f:
        config.write(f)


if __name__ == '__main__':

    # headers1 = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    # }
    #
    # headers2 = {
    #     'accept': 'application/json, text/plain, */*',
    #     # ':authority:': 'www.ralphs.com',
    #     # ':method:': 'POST',
    #     # ':path:': '/auth/api/sign-in',
    #     # ':scheme:': 'https',
    #     'accept-encoding': 'gzip, deflate, br',
    #     'accept-language': 'en-US,en;q=0.9',
    #     'cache-control': 'no-cache',
    #     'content-type': 'application/json;charset=UTF-8',
    #     # 'accept': 'application/json',
    #     'dnt': '1',
    #     'origin': 'https://www.ralphs.com',
    #     'pragma': 'no-cache',
    #     'referer': 'https://www.ralphs.com/signin?redirectUrl=/',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
    # }
    #
    # session = requests.Session()
    # session.headers.update(headers1)
    # session.get('https://www.ralphs.com/signin?redirectUrl=/')
    # time.sleep(2)
    # session.headers.update(headers2)
    # # session.headers.update({'referer': 'https://www.ralphs.com/signin?redirectUrl=/'})
    # response = session.post('https://www.ralphs.com/auth/api/sign-in', json={'email': '1@1.com', 'password': '2', 'rememberMe': True})
    # print(session.headers)
    # print(session.cookies)
    # print(response.headers)
    # print(response.raw)
    # print(response.status_code)
    # print(response.text)

    # console.print('[bold]Welcome to [dark_blue]Kroger[/dark_blue] CLI[/bold] (unofficial command line interface)')
    # if config['main']['username'] == '' or config['main']['password'] == '':
    #     console.print('In order to continue, please enter your username and password')
    #     prompt_username()