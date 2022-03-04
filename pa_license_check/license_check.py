#2021 - Angelo Poggi
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xml.etree.ElementTree as ET
from dateutil.parser import parse
from datetime import datetime, timedelta
import click
from configparser import ConfigParser
import sys

# Suppress InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# above stopped working, updating exceptions syntax
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LicenseCheck:
    def checklicensing(self,client):
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

        #All the date variables
        TodaysDate = datetime.now().date()
        WarningexpirationWindow = datetime.now().date() + timedelta(days=60)
        ErrorexpirationWindow = datetime.now().date() + timedelta(days=15)

        featureDict = {}
        featureDict['Features'] = {}
        for item in xml_response.iter():
            if 'feature' in item.tag:
                feature = item.text

            elif 'expires' in item.tag and 'Never' not in item.text:
                expires = item.text
                expires_time = parse(expires).date()
                DateValue = expires_time - TodaysDate
                WarningDaysLeft = expires_time - WarningexpirationWindow
                ErrorDaysLeft = expires_time - ErrorexpirationWindow

                #logic for OVER EXPIRED Firewalls (negative numbers)
                if DateValue.days <= 0:
                    CustomExitCode = 4
                #if TodaysDate minus Expires time IS greater thant Warning Window, No error - everything is ok!
                elif DateValue.days > 60:
                    CustomExitCode = 0
                # if todays date minus the expiration date is equal to Warning Window, throw error
                elif DateValue.days == 60:
                    featureDict['Features'][feature] = str(expires_time)
                    CustomExitCode = 1
                # if todays date minus the expiration date is less than the Warning Window AND greater than the Error window, throw the error
                # So if window is less than 60 but greater than 3
                elif DateValue.days < 60 and DateValue.days > 15 :
                    featureDict['Features'][feature] = str(expires_time)
                    CustomExitCode = 2
                # if todays date minus the expiration date IS less than error window, throw the error!
                elif DateValue.days < 15:
                    featureDict['Features'][feature] = str(expires_time)
                    CustomExitCode = 3
            else:
                continue
        #not sure why I need this here, but I do otherwise non expired clients pulls error :think:
        featureDict['Features'][feature] = str(expires_time)

        if CustomExitCode == 0:
            self._alertMessage(CustomExitCode, list(featureDict["Features"].keys()), selected_fw, featureDict['Features'][feature], DateValue.days)
        elif CustomExitCode == 1:
            self._alertMessage(CustomExitCode,list(featureDict["Features"].keys()), selected_fw, featureDict['Features'][feature])
        elif CustomExitCode == 2:
            self._alertMessage(CustomExitCode, list(featureDict["Features"].keys()), selected_fw,featureDict['Features'][feature], WarningDaysLeft.days)
        elif CustomExitCode == 3:
            self._alertMessage(CustomExitCode, list(featureDict["Features"].keys()),selected_fw,featureDict['Features'][feature], ErrorDaysLeft.days)
        elif CustomExitCode == 4:
            self._alertMessage(CustomExitCode, list(featureDict["Features"].keys()),selected_fw,featureDict['Features'][feature])

    #If CustomExitCode is 0; Everything is ok
    #If CustomExitCode is 1; Warning, Hit 60 days
    #if CustomExitCode is 2; Warning, Coutning down from 60 days
    #if CustomExitCode is 3; Error, we are less than 15 days from expiration
    #If CustomExitCode is 4; We are past expiration date

    def create_ini_file(self):
        """Creates the .ini file which stores the firewalls username and password"""
        firewall = str(input("please enter the firewall you wish to monitor\n"))
        firewallkey = str(input("please enter the Firewall Key\n"))
        client = input("Please enter the clients name, I.E. ACME\n")
        with open('fw_key.ini', 'w') as iniFile:
            iniFile.write(f"[{client}]\n")
            iniFile.write(f"key = {firewallkey}\n")
            iniFile.write(f"fw = {firewall}\n")
        click.echo("fw_key.ini file generated, you should now be able to run the script against a firewall!")

    def add_client_ini(self):
        """appends the .ini file which stores the firewalls username and password"""
        firewall = str(input("please enter the firewall you wish to monitor\n"))
        firewallkey = str(input("please enter the Firewall Key\n"))
        client = input("Please enter the clients name, I.E. ACME\n")
        with open('fw_key.ini', 'a+') as iniFile:
            iniFile.write(f"[{client}]\n")
            iniFile.write(f"key = {firewallkey}\n")
            iniFile.write(f"fw = {firewall}\n")
        click.echo("fw_key.ini file appended with new information")

    def _alertMessage(self,CustomExitCode,statement, ClientFirwall,  expirationdate, daysleft=1):
        if CustomExitCode == 0:
            print(f"{ClientFirwall} has more than {daysleft} days of Valid licensing")
            sys.exit(0)
        elif CustomExitCode == 1:
            print(f"feature set: {statement} on {ClientFirwall} has hit 60 day Expiration Mark.")
            sys.exit(1)
        elif CustomExitCode == 2:
            print(f"feature set: {statement} on {ClientFirwall} has {daysleft} before expiration.")
            sys.exit(1)
        elif CustomExitCode == 3:
            print(f"feature set: {statement} on {ClientFirwall} has less than {daysleft} before expiration.")
            sys.exit(2)
        elif CustomExitCode == 4:
            print(f"{ClientFirwall} expired! Expiration was {expirationdate}. Please order a renewal quote\nSee here to oder a quote: https://confluence.webair.com:8443/display/WO/Deploying+a+Palo+Alto+Virtual+Firewall")
            sys.exit(2)





















