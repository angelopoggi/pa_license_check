# Palo Alto License Check

Simple script to be integrated into Icinga to alert the Webair team when  firewall is set to expire in 60 days, 3 days or has already expired.

## Installation

included is a setup.py file. You can simple run

```bash
pip install --editable .
```

This will install a CLI tool called 'licensecheck'. At the moment it only has one argument '--client'.

## How it works

The primary purpose for this script was as a stop gap between implementing Panorama and the lack of system expiration date from the SNMP MIBs that are included
in netmon.

The script makes an API call to the chosen firewall and parses through the XML its returned. It grabs the feature name and the expiration date.
It checks the expiration date against the current date. If the firewall expiration date is greater than 60 days, it returns a system code of 0 which indicates
no errors. If the expiration date is within 60 days, it returns a system code of 1, prompting a warning. If the Expiration date is within 3 days, it returns a system code of 2, 
which indicates critical error. This will help give us visibility into the Palo Altos to ensure no firewall goes expired and without support from the vendor.

60 days was chosen to allow ample time for Support or the Provisioning team to request a renewal quote and proceed through the Kissflow process.

# Consideration

The script utilizes a "Cusom Exit Code" to keep track of various states. 

```text
CustomExitCode is 0; Everything is ok
CustomExitCode is 1; Warning, Hit 60 days
CustomExitCode is 2; Warning, Coutning down from 60 days
CustomExitCode is 3; Error, we are less than 3 days from expiration
CustomExitCode is 4; We are past expiration date
```

# Running the script

The script contains an .ini file which is used to store the clients firewall API key as well as the host name.
the configuration looks like this.

```bash
[webiar]
key = SuperSecureKey
fw = webair-demo-fw.gsc.hostedserver.net
```
You can then run the script as follows

```bash
licensecheck --client webair
```

it will return this sample depending on the expiration date & times

Expired Firewall
```bash
jovia-pa-fw1.gsc.hostedserver.net expired! Expiration was 2020-11-14. Please order a renewal quote
```

Firewall that is expiring within 60 days
```bash
PENDING OUTPUT
```
Firewall that is expiring within 3 days
```bash
PENDING OUTPUT
```

Firewall with valid licensing
```bash
nyserda-pa-fw1.gsc.hostedserver.net has more than 60 days of Valid licensing
```





