#(C) Webair 2021
import requests
import xml.etree.ElementTree as ET
from dateutil.parser import parse
import datetime
import click

@click.command()
@click.option('--fw', help='The FQDN of the firewall')
@click.option('--key', help='the unique key for the firewall')
def lc_check(fw,key):
    """This Script will check the specified firewall and determine its license status. You must generate an API key before usage"""
    url = f"https://{fw}/api/?type=op&cmd=<request><license><info></info></license></request>&key={key}"
    try:
        response = requests.get(url, verify=False).content
    except:
        print(f"{fw} is not reachable, please check spelling or availability")
    xml_response = ET.fromstring(response)

    todays_date = datetime.datetime.now().date()

    for item in xml_response.iter():
        if 'feature' in item.tag:
            feature = item.text
        elif 'expires' in item.tag and 'Never' not in item.text:
            expires = item.text
            expires_time = parse(expires).date()
            if todays_date >= expires_time:
                print(f"feature: {feature} has expired. Expiration date was {expires_time}")
            else:
                continue







