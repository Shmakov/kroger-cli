import configparser
import os
import click
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

    def _write_config_file(self):
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def _init_config_file(self):
        self.config.add_section('main')
        self.config['main']['username'] = ''
        self.config['main']['password'] = ''
        self.config.add_section('profile')
        self.config['profile']['first_name'] = ''
        self._write_config_file()

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def prompt_option(self):
        while True:
            self.console.print('[bold]1[/bold] - Display account info')
            self.console.print('[bold]2[/bold] - Clip all digital coupons')
            self.console.print('[bold]9[/bold] - Exit')
            option = click.prompt('Please select from one of the options', type=int)

            if option == 1:
                self._option_account_info()
            elif option == 2:
                self._option_clip_coupons()
            elif option == 9:
                return

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
            self.console.log(self.config.items(section='profile'))

    def _option_clip_coupons(self):
        self.api.clip_coupons()

    def _sign_in(self):
        if self.api.sign_in(self.username, self.password):
            self.config['main']['username'] = self.username
            self.config['main']['password'] = self.password
            self._write_config_file()
            return True
        else:
            self.console.print('[bold red]Incorrect username or password, please try again[/bold red]')
            return False

    def init(self):
        self.console.print(Panel('[bold]Welcome to [dark_blue]Kroger[/dark_blue] CLI[/bold] (unofficial command line '
                                 'interface)', box=box.ASCII))

        if self.username is None and self.config['main']['username'] != '':
            self.username = self.config['main']['username']
            self.password = self.config['main']['password']
