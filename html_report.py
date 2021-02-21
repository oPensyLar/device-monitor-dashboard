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

    def build(self, hst, wmi_object, file_path):

        procs_info = []
        cpu_usg = []
        disk_info = []

        print("[+] Found " + str(len(wmi_object.get_cpu())) + " process")

        for cpu in wmi_object.get_cpu():

            if cpu.Name == "_Total" or cpu.Name == "System" or cpu.Name == "Idle" or int(cpu.PercentProcessorTime) == 0x0:
                continue

            procs_info.append({"name": cpu.Name,
                           "pid": cpu.CreatingProcessID,
                           "mem": str(int(int(cpu.WorkingSet) / 1024/1024)) + " MB",
                           "cpu": cpu.PercentProcessorTime + " %"})

        procs_info = sorted(procs_info, key=lambda i: (i['cpu']))
        procs_info = procs_info[len(procs_info)-3:]

        for dsk in wmi_object.get_har_disks():

            if dsk.FreeSpace is not None:
                f = int(dsk.FreeSpace) / 1000000000
                f = '{0:.2g}'.format(f) + " GB"

            else:
                f = dsk.FreeSpace

            if dsk.Size is not None:
                t = int(dsk.Size) / 1000000000
                t = '{0:.2g}'.format(t)  + " GB"

            else:
                t = dsk.Size

            disk_info.append({"path": dsk.Caption,
                              "freespace": f,
                              "totalspace": t})

        t = wmi_object.get_memory()

        mem_info = {"avail_virtual": 0x0,
                    "total_virtual": 0x0,
                    "avail_phys": t["f"] + " GB",
                    "total_phys": t["t"]+ " GB"}

        self.template.stream(ip_addr=hst,
                             procs_dict=procs_info,
                             cpu_usage=cpu_usg,
                             mem_dict=mem_info,
                             disk_inf=disk_info).dump(file_path)

        return 0x0
