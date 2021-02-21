import wmi


class WmiClass:

    hds = []
    total_mem = None
    free_mem = []
    cpu_obj = None

    def get_cpu(self):
        return self.cpu_obj

    def get_har_disks(self):
        print("[+] Found " + str(len(self.hds)) + " partitions")
        return self.hds

    def get_memory(self):
            t = int(self.total_mem.TotalPhysicalMemory) / 1000000000
            t = '{0:.2g}'.format(t)

            f = int(self.free_mem.FreePhysicalMemory) / 1000000
            f = '{0:.2g}'.format(f)

            ret = {"t": t, # bytes
                   "f": f} # kilobytes
            return ret

    def set_mem_report(self, flag):
        pass

    def set_disk_report(self, flag):
        pass

    def set_procs_report(self, flag):
        pass

    def set_cpu_report(self, flag):
        pass

    def query_cpu(self, ipaddr, user, password):
        conn = wmi.WMI(ipaddr, user=user, password=password)
        self.cpu_obj = conn.Win32_PerfFormattedData_PerfProc_Process()
        return 0x0


    def query_memory(self, ipaddr, user, password):
        conn = wmi.WMI(ipaddr, user=user, password=password)

        for mem in conn.Win32_ComputerSystem():
            self.total_mem = mem

        for mem in conn.Win32_OperatingSystem():
            self.free_mem = mem

    def query_disk(self, ipaddr, user, password):
        conn = wmi.WMI(ipaddr, user=user, password=password)

        for disk in conn.Win32_LogicalDisk():
            self.hds.append(disk)

    def send_query(self, ip_addr, usr, passwd, flag):

        if flag is 0x1:
          self.query_disk(ip_addr, usr, passwd)

        if flag is 0x2:
          self.query_memory(ip_addr, usr, passwd)

        if flag is 0x3:
            self.query_cpu(ip_addr, usr, passwd)