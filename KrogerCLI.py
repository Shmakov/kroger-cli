import configparser
import os
import click
import time
from rich.console import Console
from rich.panel import Panel
from rich import box
from KrogerAPI import *


class KrogerCLI:
    config_file = 'config.ini'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.username = None
        self.password = None
        self.console = Console()
        self.api = KrogerAPI(self)
        if not os.path.exists(self.config_file):
            self._init_config_file()
        self.config.read(self.config_file)
        self.init()

    def init(self):
        if self.config['profile']['first_name'] != '':
            self.console.print(Panel('[bold]Welcome Back, ' + self.config['profile']['first_name'] + '! :smiley:\n'
                                     '[dark_blue]Kroger[/dark_blue] CLI[/bold]', box=box.ASCII))
        else:
            self.console.print(Panel('[bold]Welcome to [dark_blue]Kroger[/dark_blue] CLI[/bold] (unofficial command '
                                     'line interface)', box=box.ASCII))

        self.prompt_store_selection()

        if self.username is None and self.config['main']['username'] != '':
            self.username = self.config['main']['username']
            self.password = self.config['main']['password']
        else:
            self.prompt_credentials()

        self.prompt_options()

    def prompt_store_selection(self):
        pass
        # TODO:
        # self.console.print('Please select preferred store')

    def prompt_credentials(self):
        self.console.print('In order to continue, please enter your username (email) and password for kroger.com '
                           '(also works with Ralphs, Dillons, Smith’s and other Kroger’s Chains)')
        username = click.prompt('Username (email)')
        password = click.prompt('Password')
        self._set_credentials(username, password)

    def prompt_options(self):
        while True:
            self.console.print('[bold]1[/bold] - Display account info')
            self.console.print('[bold]2[/bold] - Clip all digital coupons')
            self.console.print('[bold]8[/bold] - Re-Enter username/password')
            self.console.print('[bold]9[/bold] - Exit')
            option = click.prompt('Please select from one of the options', type=int)

            if option == 1:
                self._option_account_info()
            elif option == 2:
                self._option_clip_coupons()
            elif option == 8:
                self.prompt_credentials()
            elif option == 9:
                return

            self.console.rule()
            time.sleep(2)

    def _write_config_file(self):
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def _init_config_file(self):
        self.config.add_section('main')
        self.config['main']['username'] = ''
        self.config['main']['password'] = ''
        self.config['main']['domain'] = 'kroger.com'
        self.config.add_section('profile')
        self.config['profile']['first_name'] = ''
        self._write_config_file()

    def _set_credentials(self, username, password):
        self.username = username
        self.password = password
        self.config['main']['username'] = self.username
        self.config['main']['password'] = self.password
        self._write_config_file()

    def _option_account_info(self):
        info = self.api.get_account_info()
        if info is None:
            self.console.print('[bold red]Couldn\'t retrieve the account info.[/bold red]')
        else:
            self.config['profile']['first_name'] = info['firstName']
            self.config['profile']['last_name'] = info['lastName']
            self.config['profile']['email_address'] = info['emailAddress']
            self.config['profile']['loyalty_card_number'] = info['loyaltyCardNumber']
            self.config['profile']['mobile_phone'] = info['mobilePhoneNumber']
            self.config['profile']['address_line1'] = info['address']['addressLine1']
            self.config['profile']['address_line2'] = info['address']['addressLine2']
            self.config['profile']['city'] = info['address']['city']
            self.config['profile']['state'] = info['address']['stateCode']
            self.config['profile']['zip'] = info['address']['zip']
            self._write_config_file()
            self.console.print(self.config.items(section='profile'))

    def _option_clip_coupons(self):
        self.api.clip_coupons()
