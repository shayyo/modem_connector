import paramiko
import _thread
import time
import json


class OpenWRTModemController:
    get_data_status_cmd = 'uqmi -d /dev/cdc-wdm1 --get-data-status'
    get_signal_info_cmd = 'uqmi -d /dev/cdc-wdm1 --get-signal-info --single'

    def __init__(self, ip, port=22, username='admin', password=''):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ssh = None
        self.type = None
        self.rssi = None
        self.rsrq = None
        self.rsrp = None
        self.snr = None
        self.connected = False

    def start(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, self.port, self.username, self.password)

        try:
            _thread.start_new_thread(self.fetch_modem_stat, ("Thread-1", 2,))
        except:
            print("Error: unable to start thread")

    def fetch_modem_stat(self, threadName, delay):
        while True:
            stdin, stdout, stderr = self.ssh.exec_command(OpenWRTModemController.get_data_status_cmd)
            gg = stdout.readline().strip().replace('"', '')
            if gg == "connected":
                self.connected = True
                stdin, stdout, stderr = self.ssh.exec_command(OpenWRTModemController.get_signal_info_cmd)
                signal_info = json.loads(stdout.readline())
                self.type = signal_info["type"]
                self.rssi = signal_info["rssi"]
                self.rsrq = signal_info["rsrq"]
                self.rsrp = signal_info["rsrp"]
                self.snr = signal_info["snr"]
            else:
                self.connected = False
                self.type = None
                self.rssi = None
                self.rsrq = None
                self.rsrp = None
                self.snr = None
            time.sleep(1)

    def print_modem_stat(self):
        if self.connected == True:
            print(f'type={modem_controller.type}\n'
                  f'rssi={modem_controller.rssi}\n'
                  f'rsrq={modem_controller.rsrq}\n'
                  f'rsrp={modem_controller.rsrp}\n'
                  f'snr={modem_controller.snr}\n')
        else:
            print("disconnected")


if __name__ == "__main__":
    modem_controller = OpenWRTModemController('192.168.1.1', username='root', password='@Password1')
    modem_controller.start()
    while True:
        modem_controller.print_modem_stat()
        time.sleep(1)
