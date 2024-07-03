import psutil
import subprocess
import datetime
import time
import os

def checkInterface(sourceInterface:str,outInterface:str):
    fullInfo=psutil.net_if_addrs()

    while True:
        try:
            fullInfo[sourceInterface]
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {sourceInterface} exists")
            break
        except KeyError:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {sourceInterface} doesn't exist")
            time.sleep(5)

    while True:
        try:
            fullInfo[outInterface]
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {outInterface} exists")
            break
        except KeyError:
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {outInterface} doesn't exist")
            time.sleep(5)

def takeDownInterface(interface:str):
    result=subprocess.call(["ip","link","set",interface,"down"])
    if result==0:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {interface} is now down")
        return True
    else:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] couldn't put {interface} down")
        return False

def runAP(ssid:str,passwd:str,outInterface:str,sourceInterface:str):
    if os.path.isdir("Logs")==False:
        os.mkdir("Logs")
    os.chdir("Logs")
    os.system(f"tmux new-session -d -s AP 'lnxrouter --ap {outInterface} {ssid} -p {passwd} -g 192.168.12.1 2>&1 | tee -a {datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}'.log")
takeDownInterface("wlan0")
runAP("RPi Network","IWishIWasALittleBitTaller","wlan0","eth0")
