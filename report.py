#!/usr/bin/python

import datetime
import json
import subprocess
import dns.resolver
from ipaddress import ip_address, ip_network
from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('template')
)

template = env.get_template('template.html.j2')


def is_ip_range(c_addr):
    var = c_addr.find("/")
    return var


def dns_resolver(ip_addr):
    my_resolver = dns.resolver.Resolver()
    nam = None

    try:
        answer = my_resolver.resolve_address(ip_addr)

    except dns.exception.Timeout:
        return nam

    for g in answer.response.answer:
        for a in g.items:
            nam = a.target
            return str(nam)


def os_detect(ttl_val):
    if ttl_val is 64:
        return "Linux"

    if ttl_val == 128:
        return "Windows"


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
def createhtml(output_file_name, host_dict):
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
                    host_dict=host_dict).dump('index.html')

# Modifica las variables del dict
def main():
    f_nam = "srv.txt"
    output_file_name = "index.html"
    hosts = []

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
        print("[+] Checking " + h.get("hostname"))

        std_out, std_error = run_ping2(h.get("hostname"))
        ping_vals = parse_output_ping(std_out)

        h.update(ip_addr=h.get("hostname"))

        if ping_vals["ttl"] is not 0x0:
            h.update(status="up")       # Vive
            dns_nam = dns_resolver(h.get("hostname"))
            os_nam = os_detect(ping_vals["ttl"])
            h.update(dns_name=dns_nam)
            h.update(os=os_nam)

        else:
            h.update(status="down")     # Dead
            h.update(dns_name="None")
            h.update(os="Unknow")

    createhtml(output_file_name, hosts)


if __name__ == "__main__":
    print(f"[INFO] {datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')} Checking hosts...")
    main()
    print(f"[INFO] {datetime.datetime.now().strftime('%b %d %Y %H:%M:%S')} Finished checking hosts")