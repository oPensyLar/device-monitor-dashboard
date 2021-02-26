from jinja2 import Environment, FileSystemLoader
import json


class HtmlReport:
    root_path = None
    env = Environment(loader=FileSystemLoader('template'))
    template = env.get_template('template-details.html.j2')

    def set_path(self, path):
        root_path = path

    def __init__(self):
        pass

    def build(self, hst, wmi_object, file_path, linux_inf):

        if wmi_object.get_error() is not 0x0:
            return

        procs_info = []
        cpu_usg = []
        disk_info = []

        print("[+] Found " + str(len(wmi_object.get_cpu())) + " process")

        for cpu in wmi_object.get_cpu():
            if cpu.Name == "_Total" or cpu.Name == "System" or cpu.Name == "Idle" or int(cpu.PercentProcessorTime) == 0x0:
                continue

            if linux_inf is True:
                mem = cpu.WorkingSet + " %"

            else:
                mem = str(int(int(cpu.WorkingSet) / 1024/1024)) + " MB"

            procs_info.append({"name": cpu.Name,
                           "pid": cpu.CreatingProcessID,
                           "mem": mem,
                           "cpu": cpu.PercentProcessorTime + " %"})

        procs_info = sorted(procs_info, key=lambda i: (i['cpu']))
        procs_info = procs_info[len(procs_info)-3:]

        for dsk in wmi_object.get_har_disks():
            if dsk.FreeSpace is not None:
                if linux_inf is 0x0:
                    f = str(int(int(dsk.FreeSpace) / 1000000000)) + " GB"

                else:
                    f = dsk.FreeSpace

            else:
                f = dsk.FreeSpace

            if dsk.Size is not None:
                if linux_inf is 0x0:
                    t = str(int(int(dsk.Size) / 1000000000)) + " GB"

                else:
                    t = dsk.Size

            else:
                t = dsk.Size

            disk_info.append({"path": dsk.Caption,
                              "freespace": f,
                              "totalspace": t})

        t = wmi_object.get_memory()

        if linux_inf is 0x0:
            f = t["f"] + " GB"
            t = t["t"] + " GB"

        else:
            f = t["f"]
            t = t["t"]

        mem_info = {"avail_virtual": 0x0,
                    "total_virtual": 0x0,
                    "avail_phys": f,
                    "total_phys": t}

        self.template.stream(ip_addr=hst,
                             procs_dict=procs_info,
                             cpu_usage=cpu_usg,
                             mem_dict=mem_info,
                             disk_inf=disk_info).dump(file_path)

        return 0x0

