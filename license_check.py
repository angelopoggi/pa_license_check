#(C) Webair 2021
import requests
import xml.etree.ElementTree as ET
from dateutil.parser import parse
from datetime import datetime, timedelta
import click
from configparser import ConfigParser
import sys
import json


@click.command()
@click.option('--client', help='Client name as defined in the fw_key.ini file')
def lc_check(client):
    """This Script will check the specified firewall and determine its license status. You must generate an API key before usage"""
    fw_config = ConfigParser()
    try:
        fw_config.read('fw_key.ini')
    except:
        print('error reading fw_key.ini file! Make sure that it exsits')
    selected_fw = fw_config.get(section=client, option='fw')
    selected_key = fw_config.get(section=client, option='key')

    url = f"https://{selected_fw}/api/?type=op&cmd=<request><license><info></info></license></request>&key={selected_key}"
    try:
        response = requests.get(url, verify=False).content
    except:
        print(f"{selected_fw} is not reachable, please check spelling or availability")
    xml_response = ET.fromstring(response)

    expirationWindow = datetime.now().date() + timedelta(days=60)

    featureDict = {}
    featureDict['Features'] = {}
    for item in xml_response.iter():
        if 'feature' in item.tag:
            feature = item.text

        elif 'expires' in item.tag and 'Never' not in item.text:
            expires = item.text
            expires_time = parse(expires).date()
            
            if expirationWindow > expires_time:
                featureDict['Features'][feature] = str(expires_time)
                definedExitCode = 1

            else:
                definedExitCode = 0
        else:
            continue
    print(definedExitCode)
    
    if definedExitCode == 1:
            alertMessage(definedExitCode,list(featureDict["Features"].keys()), featureDict["Features"][feature])
    elif definedExitCode == 0:
        alertMessage(definedExitCode, f"{selected_fw} has valid licensing")


def alertMessage(exitcode,statement1, *args):
    if exitcode == 1:
        print(f"feature: {statement1} has expired. Expiration date was {args}")
        sys.exit(1)
    elif exitcode == 0:
        print(statement1)
        sys.exit(0)






