from KrogerCLI import *
import click
# Required for pyinstaller
import six
import packaging
import packaging.version
import packaging.requirements
import packaging.specifiers
import pkg_resources

cli = KrogerCLI()


@click.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True)
def prompt_credentials(username, password):
    cli.set_credentials(username, password)


if __name__ == '__main__':
    if cli.username is None or cli.password is None:
        cli.console.print('In order to continue, please enter your username (email) and password')
        prompt_credentials()

    cli.prompt_option()