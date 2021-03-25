# device-monitor-dashboard

Welcome to the device-monitor-dashboard! Feel free to edit and contribute!


This works SSH or WMI uniques credentials for all hosts (Active Directory enviroments)


# Deploying

### Packages


You need...

- Python3 (Anaconda works)
- paramiko python package (You need install Visual Studio Build tools before)
- Edit srv.txt (for SSH/WMI monitor)
- Edit webserver.txt (for web service monitor)



### Credentials WMI/SSH

Password store under Base64 on config.json

For generate base64 code you need base64 tool & change this config.json



![Generate Base64 string](/img/base64-tool.png "Generate Base64 string").

On config.json line 6 edit you password

![Change Base64 on config.json](/img/base64-tool.png "Change Base64 on config.json").


### Whats this?

Python script to generate html report of devices, WITHOUT SOCKET AGENT!
This can be used for for servers, networking equipment, IOT devices, anything that's "pingable".
Supports:

 * OS version buid, install date, uptime report
 * WMI + SSH password encryption
 * OS fingerprint recon (Windows or Linux distro)
 * Mail notifications (SMTP relay)
 * Agent report (via socket - Only Windows support - experimental) 
 * HTTP return code (404, 200, 302)
 * IP ranges scan (192.168.0.0/24)
 * DNS name resolver (google.com -> 8.8.8.8)
 * Hostname (AD) resolver (server-win2k12.domain -> 10.0.1.122)
 * Hard disk usage report
 * Top process CPU usage
 * Memory RAM usage



## Changelog
---
 - (3/05/2020) OS version buid, uptime report
 - (2/25/2020) Added SSH + WMI password "encryption"
 - (2/22/2020) Added SMTP relay
 - (2/21/2020) Added WMI queries
 - (5/16/2020) Update to python 3
 - (9/9/2018) Replace txt file format with json
 - (1/30/2018) Replace trunicates with jinja templating engine
 - (1/27/2018) Added python 3 compatibility
 - (10/27/2017) Updated UI, noty.js
 - (9/25/2017) Add support for custom names
 - (5/27/2017) - Please see https://github.com/shaggyloris/Device-Monitor-Dashboard for extended functionality.
   - Integrated SQLite DB, all controlled via web UI, API functionality to return JSON.
 - (5/6/17) Added validation of OS for script to run
 - (2/26/17) Update Easy Install to automatically install packages
 - (2/25/17) Added support for vertically scrolling table, adjusts circle size if on mobile device.
 - (2/24/17) Combined ping function to single file, added ability to check other ports. Also converted script to be more in line with python norms. Table rows now act as hyperlinks to address listed and will auto detect port if specified.
 - (2/20/17) Updated noty,jquery, notifications UI, mobile UI
 - (2/18/17) Added support to build custom docker container
 - (2/4/17) Easy Install script now supports Node.js, update wheel color
 - (2/3/17) Change status from online/offline text to colored orb indicators


## Screenshots
---
![alt text](https://i.imgur.com/TPZsef6.png)
![alt text](https://i.imgur.com/PbmueJq.png)
