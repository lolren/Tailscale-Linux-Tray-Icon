import subprocess
import os
import sys
import time
import urllib.request
from pathlib import Path
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction



exit_node="100.78.226.7"
external_ip_to_check_against="195.62.195.246"



run_times = 0

# get current path of running directory
current_path = Path(__file__).parent
connected_image_path = current_path / 'connected.png'
disconnected_image_path = current_path / 'disconnected.png'

# create a tray icon and menu
app = QApplication(sys.argv)
tray_icon = QSystemTrayIcon()
tray_menu = QMenu()

# create actions for tray menu
connect_action = QAction("Connect", tray_menu)
disconnect_action = QAction("Disconnect", tray_menu)
exit_action = QAction("Exit", tray_menu)

def connection_status () :
    external_ip = urllib.request.urlopen('https://ipinfo.io/ip').read().decode('utf8')
    if external_ip == external_ip_to_check_against:
     print("Connected!")
     tray_icon.setIcon(QIcon(str(connected_image_path)))
     #tray_icon.setIcon(QIcon("/home/lolren/TailscalePython/connected.png"))
     subprocess.run(["notify-send", "-t", "2000","Succesfully connected, external IP:{}".format(external_ip)])
     #tray_icon.setIcon(QIcon(connect_image_path))
     #tray_icon.setToolTip(external_ip)
     tray_icon.setToolTip("Tailscale VPN Connected! external IP: {}".format(external_ip))
     connect_action.setEnabled(False)
     disconnect_action.setEnabled(True)

    else:
     print("Not Connected!")
     tray_icon.setIcon(QIcon(str(disconnected_image_path)))
     #tray_icon.setIcon(QIcon("/home/lolren/TailscalePython/disconnected.png"))
     if run_times == 1 : subprocess.run(["notify-send", "-t", "2000","VPN disconnected, external IP:{}".format(external_ip)])
     #tray_icon.setIcon(QIcon(disconnect_image_path))
     #tray_icon.setToolTip(external_ip)
     tray_icon.setToolTip("Tailscale VPN Disconnected! external IP: {}".format(external_ip))
     disconnect_action.setEnabled(False)
     connect_action.setEnabled(True)



connection_status ()

# function to connect to VPN
def connect_vpn():
    #showing a notification
    subprocess.run(["notify-send", "-t", "2000",'"Starting tailscale service"'])
    #enable tailscale systemd service
    subprocess.run(["sudo", "systemctl", "start","tailscaled.service"]) #pkexec can replace sudo here
    subprocess.run(["notify-send", "-t", "8000","Connecting to exit node:{}".format(exit_node)])
    # connect to VPN
    subprocess.run(["sudo", "tailscale", "up", "--exit-node={}".format(exit_node)])
    external_ip = urllib.request.urlopen('https://ipinfo.io/ip').read().decode('utf8')
    print(external_ip)
    # check if connection was successful
    connection_status ()
    run_times = 1

# function to disconnect from VPN
def disconnect_vpn():
    subprocess.run(["notify-send", "-t", "2000",'"Disconnecting VPN"'])
    # disconnect from VPN
    subprocess.run(["sudo", "tailscale", "down"]) #pkexec can replace sudo here
   # time.sleep(3)
    subprocess.run(["sudo", "tailscale", "up", "--reset"])
    subprocess.run(["notify-send", "-t", "2000",'"Stopping tailscale service"'])
    subprocess.run(["sudo", "systemctl", "stop","tailscaled.service"])
    connection_status ()
    run_times = 1


def app_exit():
    disconnect_vpn ()
    subprocess.run(["sudo", "tailscaled", "-cleanup"])
    app.exit ()
    subprocess.run(["notify-send", "-t", "2000",'"VPN Stopped. Will close tray!"'])
    print("will now exit!")


# add actions to tray menu
tray_menu.addAction(connect_action)
tray_menu.addAction(disconnect_action)
tray_menu.addSeparator()
tray_menu.addAction(exit_action)

# set tray icon and menu
tray_icon.setContextMenu(tray_menu)
tray_icon.show()

# connect action signals to functions
connect_action.triggered.connect(connect_vpn)
disconnect_action.triggered.connect(disconnect_vpn)
exit_action.triggered.connect(app_exit)


# start event loop
sys.exit(app.exec_())
