# device-monitor-dashboard

Python script to generate html report of devices' online/offline status. A cheap/fun reporting solution.
This can be used for for servers, networking equipment, IOT devices, anything that's "pingable".
Supports:

 * Agent support (via socket - Windows) 
 * HTTP return code (404, 200, 302)
 * IP ranges scan
 * DNS name resolver
 * Hard disk report (via WMI queries)
 * Top process CPU usage (via WMI queries)
 * Memory RAM usafe (via WMI queries)



## Changelog
---
 - (2/21/2020) Integrate WMI queries
 - (5/16/2020) Update to python 3
 - (9/9/2018) Replace txt file format with json
 - (1/30/2018) Replace trunicates with jinja templating engine
 - (1/27/2018) Added python 3 compatibility
 - (10/27/2017) Updated UI, noty.js
 - (9/25/2017) Add support for custom names
 - (6/3/2017) Now providing a docker image instead of building your own
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
![alt text](https://i.imgur.com/dx3XabN.png)
![alt text](https://i.imgur.com/k49MfS4.png)
