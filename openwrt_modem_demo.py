import time
import openwrt_modem_controller.openwrt_modem_controller as mcont

if __name__ == "__main__":
    modem0_controller = mcont.OpenWRTModemController(0, '192.168.1.1', username='root', password='@Password1')
    modem0_controller.start()
    modem1_controller = mcont.OpenWRTModemController(1, '192.168.1.1', username='root', password='@Password1')
    modem1_controller.start()
    while True:
        modem0_controller.print_modem_stat()
        modem1_controller.print_modem_stat()
        time.sleep(1)
