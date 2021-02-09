#(C) Webair 2021
import requests
import xml.etree.ElementTree as ET
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import click
from configparser import ConfigParser

@click.command()
@click.option('--client', help='Client name as defined in the fw_key.ini file')
def lc_check(client):
    fw_config = ConfigParser()
    fw_config.read('fw_key.ini')
    selected_fw = fw_config.get(section=client, option='fw')
    selected_key = fw_config.get(section=client, option='key')

    """This Script will check the specified firewall and determine its license status. You must generate an API key before usage"""
    url = f"https://{selected_fw}/api/?type=op&cmd=<request><license><info></info></license></request>&key={selected_key}"
    try:
        response = requests.get(url, verify=False).content
    except:
        print(f"{selected_fw} is not reachable, please check spelling or availability")
    xml_response = ET.fromstring(response)

    expirationWindow = datetime.now().date() + timedelta(days=60)


    for item in xml_response.iter():
        if 'feature' in item.tag:
            feature = item.text
        elif 'expires' in item.tag and 'Never' not in item.text:
            expires = item.text
            expires_time = parse(expires).date()

            if expirationWindow >= expires_time:
                print(f"feature: {feature} has expired. Expiration date was {expires_time}")
            else:
                continue







