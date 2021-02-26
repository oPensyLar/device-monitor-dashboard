import re

class Hds:
    Caption = None
    Size = None
    FreeSpace = None


class Procs:
    Name = None
    CreatingProcessID = None
    PercentProcessorTime = None
    WorkingSet = None


class Parser:

    mem = None
    err_code = None
    procs = []
    hds = []

    def get_memory(self):
        return self.mem

    def get_har_disks(self):
        self.hds = self.hds[-4:]
        return self.hds

    def get_error(self):
        return self.err_code

    def get_cpu(self):
        return self.procs

    def parse_df(self, raw_df):
        break_lines = raw_df.split("\n")

        break_lines.pop(0)
        break_lines.pop(0)

        for c_line in break_lines:
            spaces_lines = c_line.split(" ")
            index = 0x0
            one_hd = Hds()

            for one_line in spaces_lines:
                if len(one_line) > 1:
                    index += 1

                    if index is 0x1:
                        one_hd.Caption = one_line

                    if index is 0x2:
                        one_hd.Size = one_line

                    if index is 0x3:
                        one_hd.FreeSpace = one_line

            self.hds.append(one_hd)

    def parse_connections(self, raw_conns):
        pass

    def print_procs(self, procs_dict):
        print(procs_dict)

    def parse_procs(self, raw_procs):
        break_lines = raw_procs.split("\n")

        array_procs = []
        all_proc_cpu = []
        one_proc = Procs()
        semi_parse = []

        i = 0x0

        # Itera cada salto de linea
        for line in break_lines:

            if i > 0x0:
                # Itera cada elemento por linea
                for un_spacio in line.split(" "):
                    if len(un_spacio) > 0x0 and un_spacio is not " ":
                        semi_parse.append(un_spacio)

                user = semi_parse[0]
                mem = semi_parse[3]
                vsz = semi_parse[4]
                rss = semi_parse[5]
                tty = semi_parse[6]
                stat = semi_parse[7]
                param0 = semi_parse[9]

                one_proc = Procs()

                one_proc.Name = semi_parse[10]
                one_proc.CreatingProcessID = semi_parse[1]

                one_proc.PercentProcessorTime = str(int(float(semi_parse[2])))
                one_proc.WorkingSet = semi_parse[3]

                self.procs.append(one_proc)

                semi_parse.clear()

            i += 1

        return 0x0

    def parse_mem(self, raw_mem):
        break_lines = raw_mem.split("\n")

        mem_line = break_lines[2]
        swap_line = break_lines[3]

        iter = re.finditer(r"[{0-9}].[{0-9}][A-Z]", mem_line)
        indices = [m.start(0) for m in iter]

        total = mem_line[indices[0]:]
        cut_final = total.find(" ")
        total = total[:cut_final]

        usage = mem_line[indices[1]:]
        cut_final = usage.find(" ")
        usage = usage[:cut_final]

        free = mem_line[indices[2]:]
        cut_final = free.find(" ")
        free = free[:cut_final]

        self.mem = {"t": total, "f": free, "u": usage}


    def set_error(self, error_code):
        self.err_code = error_code

    def parse_output(self, output):
        output = output["stdout"]
        raw_ssh_data = output.split("--C0RT4--")

        ps_cpu = raw_ssh_data[0]
        self.parse_procs(ps_cpu)

        # self.parse_procs(ps_mem, 0x4)

        # free = raw_ssh_data[3]
        self.parse_mem(raw_ssh_data[10])

        netstat = raw_ssh_data[4]
        self.parse_connections(netstat)

        df = raw_ssh_data[12]
        self.parse_df(df)