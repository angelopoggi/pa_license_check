# Palo Alto License Check

Simple script to be integrated into Icinga to alert the Webair team when  firewall is set to expire in 60 days, 3 days or has already expired.

## Installation

You can install this through PyPI using pip
```bash
pip install pa-license-check
```

This will install a CLI tool called 'palicensecheck'. It will allow you to do the following

1 - Create an INI file that it uses to read the firewall
2 - Adds new clients to the INI File
3 - Checks the licensing status and returns an exit code

## How it works

The primary purpose for this script was as a stop gap between implementing Panorama and the lack of system expiration date from the SNMP MIBs that are included
in Monitoring Software like LibreNMS.

The script makes an API call to the chosen firewall and parses through the XML its returned. It grabs the feature name and the expiration date.
It checks the expiration date against the current date. If the firewall expiration date is greater than 60 days, it returns a system code of 0 which indicates
no errors. If the expiration date is within 60 days, it returns a system code of 1, prompting a warning. If the Expiration date is within 3 days, it returns a system code of 2, 
which indicates critical error. This will help give us visibility into the Palo Altos to ensure no firewall goes expired and without support from the vendor.

60 days was chosen to allow ample time for Support or the Provisioning team to request a renewal quote and proceed through the Kissflow process.

# Custom Exit Codes

The script utilizes a "Cusom Exit Code" to keep track of various states. This is not to be confused with the system exit codes, which are used to tell Icinga what severity.
This is strictly for keeping track within the function itself! I decided to Document it in case anyone wanted to expand on this.

```text
CustomExitCode is 0; Everything is ok
CustomExitCode is 1; Warning, Hit 60 days
CustomExitCode is 2; Warning, Coutning down from 60 days
CustomExitCode is 3; Error, we are less than 3 days from expiration
CustomExitCode is 4; We are past expiration date
```

# Running the script

## Generating INI File
---

On the first initial run, you'll need to build the INI file. You can easily do this by running

```bash
palicensecheck create-ini-file
```

It will then ask you a series of questions

```text
please enter the firewall you wish to monitor
hank.kingofthe.hill
please enter the Firewall Key
wah5eeGhee7thah2waechohshai6ah6iphugh4ahpoophaeva0aeTutah6ohSooPopane
Please enter the clients name, I.E. ACME
Strikland
```

It will then create the INI file in the root directory of the script
Which will look like this.

```text
['Strikland']
key = wah5eeGhee7thah2waechohshai6ah6iphugh4ahpoophaeva0aeTutah6ohSooPopane
fw = hank.kingofthe.hill
```

## Adding clients to the INI file

You can easily add new clients to the INI file by running the following command

```bash
palicensecheck add-client-ini
```

It will then walk you through a series of questions to help build the file.

```bash
please enter the firewall you wish to monitor
thatherton.fueles.demo
please enter the Firewall Key
oogoo1eec0ef0ong2ix0sheingughae8oongiebaicee3que0ShaD6rau0Looch9
Please enter the clients name, I.E. ACME
thatherton
fw_key.ini file appended with new information
```

here we can see the expanded file

```text
[strikland]
key = wah5eeGhee7thah2waechohshai6ah6iphugh4ahpoophaeva0aeTutah6ohSooPopane
fw = hank.kingofthe.hill
[thatherton]
key = oogoo1eec0ef0ong2ix0sheingughae8oongiebaicee3que0ShaD6rau0Looch9
fw = thatherton.fueles.demo
```

## Checking the license Status

To run the script and check the status, simply run the following command

```bash
palicensecheck check-license --client strikland
```

Its important to remember that the argument after the --client param **must** match the group name in your INI file.

# To Do

I cobbled this together to what it is today in a few hours time updating it.
Please let me know if there are bugs, issues or any features you would like added.

* Need to do testing against firewall that is online
* Need to adjust some error catching


