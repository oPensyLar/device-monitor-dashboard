# device-monitor-dashboard

Python script to generate html report of devices, WITHOUT SOCKET AGENT! This can be used for for servers, networking equipment, IoT devices, anything that's "pingable".


This works SSH or WMI uniques credentials for all hosts (Active Directory enviroments)


# Deploying



### Notes

- Python3 (Anaconda works)
- for Windows test need you install Visual Studio Build tools (paramiko package requeriment)
- Edit srv.txt (for SSH/WMI monitor)
- Edit webserver.txt (for web service monitor)

After this you already for install Python package dependecies


```
pip -r requeriments.txt
```

Now ran ...

```
python report.py
```


### Credentials WMI/SSH

Password store under Base64 on config.json

For generate base64 code you need base64 tool & change this config.json



![Generate Base64 string](/img/base64-tool.png "Generate Base64 string").

On config.json ** line 6 ** change **cHhndHNqbW50** to **c3VwZXJfcGFzc3dvcmQ=**

![Change Base64 on config.json](/img/password-config-json.png "Change Base64 on config.json").





### Mail notification support

You can disable/enable on report.py ** line 196 **



```python
def main():
    mail_notification = False
```


### websever.txt format


```
192.168.1.3
127.0.0.1
hostname.domain
www.google.com
```


# Features

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
