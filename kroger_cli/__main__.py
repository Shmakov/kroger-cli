import click
from kroger_cli.cli import KrogerCLI

kroger_cli = KrogerCLI()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--disable-headless', is_flag=True, help='Disable chromium\'s headless mode (useful for debug).')
def cli(ctx, disable_headless):
    if disable_headless:
        kroger_cli.api.browser_options['headless'] = False

    # CLI call without a command
    if ctx.invoked_subcommand is None:
        kroger_cli.prompt_options()


@click.command('account-info', help='Display account info.')
def account_info():
    kroger_cli.option_account_info()


@click.command('clip-coupons', help='Clip all digital coupons.')
def clip_coupons():
    kroger_cli.option_clip_coupons()


@click.command('purchases-summary', help='Purchases Summary.')
def purchases_summary():
    kroger_cli.option_purchases_summary()


@click.command('points-balance', help='Retrieve Points Balance.')
def points_balance():
    kroger_cli.option_points_balance()


@click.command('survey', help='Complete Kroger’s Survey (to earn 50 points).')
def survey():
    kroger_cli.option_survey()


if __name__ == '__main__':
    cli.add_command(account_info)
    cli.add_command(clip_coupons)
    cli.add_command(purchases_summary)
    cli.add_command(points_balance)
    cli.add_command(survey)

    cli()
