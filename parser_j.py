import json


class json_parser:

    mem_report = 0x0
    cpu_report = 0x0
    procs_report = 0x0
    disk_repot = 0x0
    pass_auth = None

    def __init__(self):
        pass

    def set_cpu_report(self, flag):
        self.cpu_report = flag

    def set_pass_auth(self, pwd):
        self.pass_auth = pwd

    def set_mem_report(self, flag):
        self.mem_report = flag

    def set_disk_report(self, flag):
        self.disk_report = flag

    def set_procs_report(self, flag):
        self.procs_report = flag

    def build_request(self):
        req_dict = {}
        req_dict["req"] = {"auth": {"pass" : self.pass_auth},
                           "procs": self.procs_report,
                           "disk": self.disk_report,
                           "mem": self.mem_report,
                           "cpu": self.cpu_report}
        return req_dict

    def get_request(self):

        return json.dumps(self.build_request())

