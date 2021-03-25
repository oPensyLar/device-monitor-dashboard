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

![Change Base64 on config.json](/img/password-config-json.png "Change Base64 on config.json").


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


## Screenshots
---

HTML general
![Screenshot index](https://i.imgur.com/TPZsef6.png)

HTML by host
![Screenshot details](https://i.imgur.com/PbmueJq.png)
