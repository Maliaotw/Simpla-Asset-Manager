

from .base import BasePlugin


class CpuPlugin(BasePlugin):

    def windows(self):
        data = {}
        cpu_lists = self.wmi_obj.Win32_Processor()
        cpu_core_count = 0

        for cpu in cpu_lists:
            cpu_core_count += cpu.NumberOfCores
            cpu_model = cpu.Name
        data["cpu_count"] = len(cpu_lists)
        data["cpu_model"] = cpu_model
        data["cpu_core_count"] = cpu_core_count
        return data

    def linux(self):
        base_cmd = 'cat /proc/cpuinfo'

        raw_data = {
            'cpu_model': "%s |grep 'model name' |head -1 " % base_cmd,
            'cpu_count': "%s |grep  'processor'|wc -l " % base_cmd,
            'cpu_core_count': "%s |grep 'cpu cores' |awk -F: '{SUM +=$2} END {print SUM}'" % base_cmd,
        }

        for k, cmd in raw_data.items():
            try:
                # cmd_res = subprocess.check_output(cmd,shell=True)
                cmd_res = self.exec_shell_cmd(cmd)
                raw_data[k] = cmd_res.strip()

            # except Exception,e:
            except ValueError as e:
                print(e)

        data = {
            "cpu_count": raw_data["cpu_count"],
            "cpu_core_count": raw_data["cpu_core_count"]
        }
        cpu_model = raw_data["cpu_model"].split(":")
        if len(cpu_model) > 1:
            data["cpu_model"] = cpu_model[1].strip()
        else:
            data["cpu_model"] = -1

        return data






