#!/usr/bin/python

import datetime
import json
import socket
import subprocess
from ipaddress import ip_address, ip_network
from jinja2 import Environment, FileSystemLoader
import dns.resolver
import socket_client
import html_report
import compress
import ssh_client
import mailer
import os
import requests
import wmi_class
import util
import _parser
import re

env = Environment(loader=FileSystemLoader('template'))
template = env.get_template('template.html.j2')

def domain_checker(domain):
    pattern = re.compile('(//|\s+|^)(\w\.|\w[A-Za-z0-9-]{0,61}\w\.){1,3}[A-Za-z]{2,6}')
    ret = pattern.match(domain)
    return ret


def ip_checker(ip_addr):
    pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    return pattern.match(ip_addr)


def load_config(file_path):
    with open(file_path, "r") as f:
        cfg = json.load(f)
        return cfg


def build_zip(c_path, file_path_output):
    c = compress.Compress()
    css_folder = c_path + "\\css"
    js_folder = c_path + "\\js"
    report_folder = c_path + "\\report-details"
    arrays_files = [report_folder, css_folder, js_folder, "index.html"]
    c.build(c_path, arrays_files, file_path_output)


def send_mail(mail_data, user_data, server_data):
    m = mailer.Mailer()

    m.set_login(user_data.get("sender"))
    m.set_srv(server_data.get("serv"), server_data.get("port"))
    m.set_body(mail_data.get("to"),
               mail_data.get("subject"),
               mail_data.get("attach"),
               mail_data.get("body"))

    m.conn()


def check_web(hst, ports):

    ret_data = []
    resp = None
    for port in ports:

        if port == 443:
            protocol = "https"

        else:
            protocol = "http"

        try:
            url = protocol + "://" + hst + ":" + str(port)
            resp = requests.get(url, verify=False)
            http_code = resp.status_code

        except requests.exceptions.ConnectionError:
            if resp is None:
                http_code = "N/A"
            else:
                if port == 80:
                    http_code = "N/A"

                else:
                    http_code = resp.status_code

        dat_obj = {"host": hst, "port": port, "code": http_code}
        ret_data.append(dat_obj)

    return ret_data


def is_ip_range(c_addr):
    var = c_addr.find("/")
    return var


def dns_resolver(ip_addr):
    my_resolver = dns.resolver.Resolver()
    nam = None

    try:
        answer = my_resolver.resolve_address(ip_addr)

    except dns.exception.Timeout:
        return None

    except dns.resolver.NXDOMAIN:
        return None

    for g in answer.response.answer:
        for a in g.items:
            nam = a.target
            return str(nam)


def os_detect(ttl_val):
    if ttl_val is 64 or ttl_val is 60:
        return "Linux"

    if ttl_val == 128 or ttl_val == 124:
        return "Windows"

    return "N/A"


def parse_output_ping(output_string):
    output_string = output_string.decode("utf-8")

    ttl_numb = "0"

    if output_string.find("TTL") > 0x0:
        # Begin TTL extraction
        pos_init = output_string.find("TTL")
        pos_init += 4
        output_string = output_string[pos_init:]
        output_string_split = output_string.split("\r")
        ttl_numb = output_string_split[0]
        # End TTL extraction

    ret = {"ttl": int(ttl_numb)}
    return ret


def run_ping2(hst):
    array_program = ["ping", "-n", "1", hst]
    h = subprocess.Popen(array_program, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return h.communicate()


def parsehost(hostfile):
    servers = []
    with open(hostfile, "r") as f:
        data = json.load(f)

        for item in data:
                if item["alias"]:
                    servers.append({"hostname": item["url"], "name": item["alias"]})
                else:
                    servers.append({"hostname": item["url"], "name": item["url"]})
    return servers


# host_dict Ya esta creado, mete las variables en el HTML
def createhtml(output_file_name, host_dict, wserver_dict):
    refresh_rate = "60"
    today = (datetime.datetime.now())
    now = today.strftime("%m/%d/%Y %H:%M:%S")
    servers_up = 0.00
    servers_down = 0.00
    servers_percent = 0.00

    for h in host_dict:
        if h.get("status") == "up":
            servers_up += 1
        else:
            servers_down += 1
    server_total = (servers_up + servers_down)
    servers_percent = str(round((((server_total) - servers_down) / (server_total)), 2))

    template.stream(refresh_rate=refresh_rate,
                    today=today, now=now,
                    servers_up=servers_up,
                    servers_down=servers_down,
                    servers_percent=servers_percent,
                    server_total=server_total,
                    web_host_dict=wserver_dict,
                    host_dict=host_dict).dump('index.html')


def main():
    mail_notification = False

    c_wmi = wmi_class.WmiClass()
    ssh = ssh_client.SshClient()
    utils = util.Util()

    webservers_file_path = "webserver.txt"
    f_nam = "srv.txt"
    output_file_name = "index.html"
    hosts = []
    webserver_hosts = []

    config = load_config("config.json")

    # WMI user/pass
    wmi_user = utils.b64_decrypt(config.get("wmi").get("user"))
    wmi_pwd = utils.b64_decrypt(config.get("wmi").get("password"))

    ssh_user = utils.b64_decrypt(config.get("ssh").get("user"))
    ssh_pwd = utils.b64_decrypt(config.get("ssh").get("password"))
    ssh_port = config.get("ssh").get("port")
    ssh_payload = utils.b64_decrypt(config.get("ssh").get("payload"))
    print("[+] Payload length:: " + str(len(ssh_payload)))

    user = config.get("mail").get("smtp").get("user")

    serv = config.get("mail").get("smtp").get("server")
    port = config.get("mail").get("smtp").get("port")

    para = config.get("mail").get("to")
    subject = config.get("mail").get("subject")

    p = _parser.Parser()

    # with open("C:\\Users\\opensylar\\Desktop\\mem_parse.log", "r") as fp:
    #    l = fp.read()
    #    p.parse_mem(l)

    with open(webservers_file_path, "r") as f:
        ports = [80, 443]

        for c_addr in f:
            c_addr = c_addr.replace("\n", "")
            c_addr = c_addr.replace("\r", "")
            print("[+] Sending web tests to " + c_addr)
            status_web = check_web(c_addr, ports)
            webserver_hosts.append(status_web)

    with open(f_nam, "r") as f:
        for c_addr in f:
            c_addr = c_addr.replace("\n", "")
            c_addr = c_addr.replace("\r", "")

            if is_ip_range(c_addr) > 0x0:
                net1 = ip_network(c_addr, strict=False)

                for addr in net1:
                    addr = str(addr)
                    hosts.append({"hostname": addr})

            else:
                hosts.append({"hostname": c_addr})

    # Setea las variables del dict
    for h in hosts:
        print("\r\n[+] Checking " + h.get("hostname"))

        std_out, std_error = run_ping2(h.get("hostname"))
        ping_vals = parse_output_ping(std_out)

        h.update(ip_addr=h.get("hostname"))

        if ping_vals["ttl"] is not 0x0:
            html_path = "report-details/details-" + h.get("hostname") + ".html"
            h.update(status="up")

            # dns_nam = dns_resolver(h.get("hostname"))

            try:
                dns_nam = socket.gethostbyaddr(h.get("hostname"))
                dns_nam = dns_nam[0]

            except socket.herror:
                dns_nam = "Unknow"

            os_nam = os_detect(ping_vals["ttl"])
            # print("TTL:: " + str(ping_vals["ttl"]))

            h.update(dns_name=dns_nam)
            h.update(os=os_nam)
            h.update(html_path=html_path)

            s = socket_client.SocketClient()
            html_rpt = html_report.HtmlReport()
            html_rpt.set_path("report-details")

            if os_nam == "Windows":
                print("[+] Sending WMI query..")

                c_wmi.send_query(h.get("hostname"), wmi_user, wmi_pwd, 0x1)
                c_wmi.send_query(h.get("hostname"), wmi_user, wmi_pwd, 0x2)
                c_wmi.send_query(h.get("hostname"), wmi_user, wmi_pwd, 0x3)
                c_wmi.send_query(h.get("hostname"), wmi_user, wmi_pwd, 0x4)

                h.update(status_agent="1")
                html_rpt.build(h.get("hostname"), c_wmi, html_path, False)

            else:
                h.update(status_agent="1")
                print("[+] Sending SSH payload..")

                c_ssh = ssh.send_query(h.get("hostname"),
                                       ssh_port,
                                       ssh_user,
                                       ssh_pwd,
                                       ssh_payload)

                html_rpt.build(h.get("hostname"), c_ssh, html_path, True)

        # Offline
        else:
            print("[!] " + h.get("hostname") + " offline")
            h.update(status_agent="0")
            h.update(status="down")     # Dead

            try:
                dns_nam = socket.gethostbyaddr(h.get("hostname"))
                dns_nam = dns_nam[0]

            except socket.herror:
                dns_nam = "Unknow"

            except socket.gaierror:
                print("[!] " + h.get("hostname") + " is bad host")
                exit(-1)

            h.update(dns_name=dns_nam)
            h.update(os="Unknow")

    createhtml(output_file_name, hosts, webserver_hosts)

    c_path = os.getcwd()
    file_output = c_path + "\\reports.zip"
    build_zip(c_path, file_output)

    if mail_notification is True:
        print("[+] Sending mail to SMTP relay server")

        u = {"sender": user}
        s = {"serv": serv, "port": port}
        m = {"to": para, "subject": subject, "attach": file_output, "body": "Report"}
        send_mail(m, u, s)

    print("[+] Finish!")


if __name__ == "__main__":
    print(f"[INFO] {datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')} Checking hosts...")
    main()
    print(f"[INFO] {datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')} Finished checking hosts")