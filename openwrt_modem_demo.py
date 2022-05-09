import time
import openwrt_modem_controller.openwrt_modem_controller as modem_cont


def state_callback(modem_no, connected):
    if connected:
        print(f'MODEM%d EVENT: connected' % modem_no)
    else:
        print(f'MODEM%d EVENT: disconnected' % modem_no)


def print_modem_stat(modem_no, modem_controller):
    print(f'******* MODEM%d STAT *******' % modem_no)
    if modem_controller.connected:
        print(f'connection-type={modem_controller.conn_type}\n'
              f'operator={modem_controller.operator}\n'
              f'rssi={modem_controller.rssi}\n'
              f'rsrq={modem_controller.rsrq}\n'
              f'rsrp={modem_controller.rsrp}\n'
              f'snr={modem_controller.snr}')
    else:
        print("disconnected")
        print('********** END *************')


if __name__ == "__main__":
    modem0_controller = modem_cont.OpenWRTModemController(0, '3-1', '192.168.1.1', username='root',
                                                          password='@Password1', modem_state_callback=state_callback)
    modem1_controller = modem_cont.OpenWRTModemController(1, '1-1.2', '192.168.1.1', username='root',
                                                          password='@Password1', modem_state_callback=state_callback)
    try:
        modem0_controller.connect()
        modem1_controller.connect()
    except:
        print('ERROR: failed connecting to router')
        exit(-1)

    while True:
        print_modem_stat(0, modem0_controller)
        print_modem_stat(1, modem1_controller)
        time.sleep(1)
