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

    def build(self, hst, dats, file_path):
        j_str = dats.decode("utf-8")
        resp_json = json.loads(dats)
        disk_info = []
        procs_info = []
        mem_info = []
        cpu_usg = None

        if resp_json["auth"].get("state"):
            for dsk in resp_json["disk"]:
                f = "{:.2f}".format(dsk["free"] / 1024)
                t = "{:.2f}".format(dsk["total"] / 1024)
                disk_info.append({"path": dsk["path"], "freespace": f, "totalspace": t})

            for m in resp_json["mem"]:
                var1 = "{:.2f}".format(m.get("total_phys") / 1073741824)
                m.update(total_phys=var1)

                var1 = "{:.2f}".format(m.get("avail_phys") / 1073741824)
                m.update(avail_phys=var1)

                var1 = "{:.2f}".format(m.get("total_virtual") / 1073741824)
                m.update(total_virtual=var1)

                var1 = "{:.2f}".format(m.get("avail_virtual") / 1073741824)
                m.update(avail_virtual=var1)
                mem_info = m

            for c in resp_json["cpu"]:
                cpu_usg = c.get("usage")

            for c_proc in resp_json["procs"]:
                var1 = int(c_proc["mem_usage"] / 1024)

                procs_info.append({"name": c_proc["nam"],
                                   "pid": c_proc["pid"],
                                   "mem": var1,
                                   "cpu": c_proc["cpu_usage"],
                                   })

            self.template.stream(ip_addr=hst,
                                 procs_dict=procs_info,
                                 cpu_usage=cpu_usg,
                                 mem_dict=mem_info,
                                 disk_inf=disk_info).dump(file_path)