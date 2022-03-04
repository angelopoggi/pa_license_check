import click

from pa_license_check.license_check import LicenseCheck

@click.group(help="""
                    Simple Script that allows you to
                    check the licensing status on a Palo Alto Firewall.\n
                    It works by returning an Exit code, which can then be read by
                    a monitoring service like Nagios or Icinga.\n
                    You can set to this a Cron Job and run it periodically.""")
def cli():
    pass

@cli.command(help="""
                    This command will allow you build the initial INI fileE""")
def create_ini_file():
    classInit = LicenseCheck()
    return classInit.create_ini_file()

@cli.command(help="""
                    This command allows you to quickly add a new client to the INI file.""")
def add_client_ini():
    classInit = LicenseCheck()
    return classInit.add_client_ini()

@cli.command()
@click.option(
    '--client', '-c', help="The group name configured in the INI",
    required=True,
    type=str
)
def check_license(client):
    classInit = LicenseCheck()
    return classInit.checklicensing(client)