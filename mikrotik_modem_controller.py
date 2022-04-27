import paramiko
import _thread
import time
#

class MikrotikModemController:
    lte_int_info_cmd = 'uci show wireless'

    def __init__(self, ip, port=22, interface_id=0, username='admin', password=''):
        self.ip = ip
        self.port = port
        self.interface_id = interface_id
        self.username = username
        self.password = password
        self.rssi = 7
        self.ssh = None

    def start(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, self.port, self.username, self.password)

        try:
            _thread.start_new_thread(self.print_stat, ("Thread-1", 2,))
        except:
            print("Error: unable to start thread")

    def print_stat(self, threadName, delay):
        while True:
            stdin, stdout, stderr = self.ssh.exec_command(MikrotikModemController.lte_int_info_cmd)
            outlines = stdout.readlines()
            print(outlines)

            time.sleep(1)


if __name__ == "__main__":
    micro_modem_controller = MikrotikModemController('192.168.1.1', username='root', password='@Password1')
    micro_modem_controller.start()
    while True:
        time.sleep(1)
