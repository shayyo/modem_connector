import paramiko
import _thread
import time
import json


class OpenWRTModemController:
    get_data_status_cmd = 'uqmi -d /dev/cdc-wdm%d --get-data-status'
    get_signal_info_cmd = 'uqmi -d /dev/cdc-wdm%d --get-signal-info --single'
    get_operator_cmd = "gsmctl -O %s --operator"

    def __init__(self, modem_no, usb_modem_id, ip, port=22, username='admin', password='', modem_state_callback=None):
        self.__modem_no = modem_no
        self.__usb_modem_id = usb_modem_id
        self.__ip = ip
        self.__port = port
        self.__username = username
        self.__password = password
        self.__modem_state_callback = modem_state_callback
        self.__ssh = None
        self.connected = False
        self.conn_type = None
        self.rssi = None
        self.rsrq = None
        self.rsrp = None
        self.snr = None
        self.operator = None

    def connect(self):
        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.__ssh.connect(self.__ip, self.__port, self.__username, self.__password)
        except:
            raise Exception("connect")

        try:
            _thread.start_new_thread(self.__fetch_modem_stat, ('fetch-modem%d-stat-thread' % self.__modem_no, 2,))
        except:
            raise Exception("new_thread")

    def __fetch_modem_stat(self, threadName, delay):
        while True:
            # exec get data status cmd
            stdin, stdout, stderr = self.__ssh.exec_command(self.get_data_status_cmd % self.__modem_no)
            if stdout.readline().strip().replace('"', '') == "connected":
                # exec get signal info cmd
                stdin, stdout, stderr = self.__ssh.exec_command(self.get_signal_info_cmd % self.__modem_no)
                signal_info = json.loads(stdout.readline())
                self.conn_type = signal_info["type"]
                self.rssi = signal_info["rssi"]
                self.rsrq = signal_info["rsrq"]
                self.rsrp = signal_info["rsrp"]
                self.snr = signal_info["snr"]
                # exec get operator cmd
                stdin, stdout, stderr = self.__ssh.exec_command(self.get_operator_cmd % self.__usb_modem_id)
                self.operator = stdout.readline().strip()
                if not self.connected and self.__modem_state_callback is not None:
                    self.__modem_state_callback(self.__modem_no, True)
                self.connected = True
            else:
                self.conn_type = None
                self.rssi = None
                self.rsrq = None
                self.rsrp = None
                self.snr = None
                self.operator = None
                if self.connected and self.__modem_state_callback is not None:
                    self.__modem_state_callback(self.__modem_no, True)
                self.connected = False
            time.sleep(5)