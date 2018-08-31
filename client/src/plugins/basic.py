

from .base import BasePlugin
import subprocess

class BasicPlugin(BasePlugin):

    def windows(self):
        pass

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

        distributor = subprocess.getoutput(" lsb_release -a|grep 'Distributor ID'").split(":")
        # release  = subprocess.check_output(" lsb_release -a|grep Description",shell=True).split(":")
        release = subprocess.getoutput(" lsb_release -a|grep Description").split(":")
        data['os_distribution'] = distributor[1].strip() if len(distributor) > 1 else None
        data['os_release'] = release[1].strip() if len(release) > 1 else None,
        data['os_type'] = "linux"


        return data






