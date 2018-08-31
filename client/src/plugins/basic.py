from .base import BasePlugin
import subprocess
import platform


class BasicPlugin(BasePlugin):

    def os_platform(self):
        """
        获取系统平台
        :return:
        """
        return platform.system()

    def os_hostname(self):
        """
        獲取電腦名稱
        :return:
        """

        pass

    def windows(self):
        import win32com
        import wmi
        wmi_obj = wmi.WMI()
        # wmi_service_obj = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        # wmi_service_connector = self.wmi_service_obj.ConnectServer(".", "root\cimv2")

        computer_info = wmi_obj.Win32_ComputerSystem()[0]
        system_info = wmi_obj.Win32_OperatingSystem()[0]
        data = {}
        data['manufactory'] = computer_info.Manufacturer
        data['model'] = computer_info.Model
        data['wake_up_type'] = computer_info.WakeUpType
        data['sn'] = system_info.SerialNumber

        data['os_type'] = platform.system(),
        data['os_release'] = "%s %s  %s " % (platform.release(), platform.architecture()[0], platform.version()),
        data['os_distribution'] = 'Microsoft'

        return data

    def linux(self):
        filter_keys = ['Manufacturer', 'Serial Number', 'Product Name', 'UUID', 'Wake-up Type']
        raw_data = {}

        for key in filter_keys:
            try:
                # cmd_res = subprocess.check_output("sudo dmidecode -t system|grep '%s'" %key,shell=True)
                cmd_res = subprocess.getoutput("sudo dmidecode -t system|grep '%s'" % key)
                cmd_res = cmd_res.strip()

                res_to_list = cmd_res.split(':')
                if len(res_to_list) > 1:  # the second one is wanted string
                    raw_data[key] = res_to_list[1].strip()
                else:

                    raw_data[key] = -1
            except Exception as e:
                print(e)
                raw_data[key] = -2  # means cmd went wrong

        data = {"asset_type": 'host'}
        data['manufactory'] = raw_data['Manufacturer']
        data['sn'] = raw_data['Serial Number']
        data['model'] = raw_data['Product Name']
        data['uuid'] = raw_data['UUID']
        data['wake_up_type'] = raw_data['Wake-up Type']

        distributor = subprocess.getoutput("lsb_release -a|grep 'Distributor ID'").split("\t")[1]
        # release  = subprocess.check_output(" lsb_release -a|grep Description",shell=True).split(":")
        release = subprocess.getoutput("lsb_release -a|grep Description").split("\t")[1]
        data['os_distribution'] = distributor
        data['os_release'] = release
        data['os_type'] = platform.system()
        data['node'] = platform.node()

        return data
