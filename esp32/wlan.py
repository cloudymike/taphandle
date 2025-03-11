# Very simple example of how to setup network
# Best run interactively
# Enter SSID and PASSWORD here or load file once and then
# run the function with the right parameters

import network
import wlanconfig
import machine
import time

def do_connect(hostname='micropythonexamples'):
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    # Add a delay for this issue in 19.1 https://github.com/micropython/micropython/issues/9236
    time.sleep_ms(100)
    nic.config(dhcp_hostname=hostname)
    time.sleep_ms(100)
    nic.connect(wlanconfig.ESSID,wlanconfig.PASSWORD)
    time.sleep_ms(100)
    if not nic.isconnected():
        print('connecting to network...')
        while not nic.isconnected():
            time.sleep_ms(100)

    print('network config:', nic.ifconfig())
    return(nic)

# Remove old connection if exist before reconnecting
def fresh_connect(hostname='micropythonexamples'):
    nic = network.WLAN(network.STA_IF)
    nic.active(True)
    if(nic.isconnected()):
        nic.disconnect()
    print('connecting to network...')
    nic = do_connect(hostname)
    return(nic)
    