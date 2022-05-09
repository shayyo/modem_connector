import paramiko
import _thread
import time
import json


class OpenWRTModemController:
    get_data_status_cmd = 'uqmi -d /dev/cdc-wdm%d --get-data-status'
    get_signal_info_cmd = 'uqmi -d /dev/cdc-wdm%d --get-signal-info --single'

    def __init__(self, modem_no, ip, port=22, username='admin', password=''):
        self.modem_no = modem_no
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
            _thread.start_new_thread(self.fetch_modem_stat, ('fetch-modem%d-stat-thread' % self.modem_no, 2,))
        except:
            print("Error: unable to start thread")

    def fetch_modem_stat(self, threadName, delay):
        while True:
            stdin, stdout, stderr = self.ssh.exec_command(OpenWRTModemController.get_data_status_cmd % self.modem_no)
            gg = stdout.readline().strip().replace('"', '')
            if gg == "connected":
                self.connected = True
                stdin, stdout, stderr = self.ssh.exec_command(OpenWRTModemController.get_signal_info_cmd % self.modem_no)
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
        print(f'******* MODEM%d *******' % self.modem_no)
        if self.connected:
            print(f'type={self.type}\n'
                  f'rssi={self.rssi}\n'
                  f'rsrq={self.rsrq}\n'
                  f'rsrp={self.rsrp}\n'
                  f'snr={self.snr}\n')
        else:
            print("disconnected")
