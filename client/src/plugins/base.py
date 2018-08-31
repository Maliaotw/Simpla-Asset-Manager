

import platform

class BasePlugin(object):

    def __init__(self):
        pass


    def chkos(self):
        '''
        判斷作業系統
        :return:
        '''

        os = platform.system()
        return os

    def execute(self):

        os = self.chkos()
        # print("os",os)

        if os == "Windows":
            return self.windows()

        elif os == "Linux":
            # print("Linux")
            return self.linux()


    def windows(self):
        pass


    def linux(self):
        pass



