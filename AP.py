import psutil
import subprocess
import datetime
import time
import os
import json

settingsFile="/boot/firmware/rpiHotspot.json"

DEFAULT=True
NOINTERNET=False

def getSettings(filePath:str):
    if os.path.isfile(filePath):
        print(f"Trying to use settings from {filePath.split('/')[-1]}...")
        try:
            with open(filePath,"r") as f:
                settings=json.load(f)
                global DEFAULT
                DEFAULT=False
                return settings
        except:
            print("Failed to load settings. Using default settings.")
    else:
        print("File not found. Using default settings.")



def parseSettings(settings:dict):
    global NOINTERNET
    settingsStr=""
    if settings.get("interfaceOut"):
        print(f"Using provided out interface: {settings.get('interfaceOut')}")
        if settings.get("ssid"):
            print(f"Using provided SSID: {settings.get('ssid')}")
            settingsStr+=f"--ap {settings.get('interfaceOut')} {settings.get('ssid')} "
        else:
            print("SSID not specified. Using default settings.")
            settingsStr+=f"--ap {settings.get('interfaceOut')} RPiHotspot "
    else:
        print("Out interface is not specified. Defaulting to wlan0")
        if settings.get("ssid"):
            settingsStr+=f"--ap wlan0 {settings.get('ssid')} "
        else:
            print("SSID not specified. Using default settings.")
            settingsStr+=f"--ap wlan0 RPiHotspot "

    if settings.get("isolate-clients"):
        print("isolate-clients is set to true.")
        settingsStr+="--isolate-clients "

    if settings.get("interfaceIn"):
        print(f"Using provided interface to get connection from: {settings.get('interfaceIn')}")
        settingsStr+=f"-o {settings.get('interfaceIn')} "
    else:
        print("No input interface specified. Will receive connections from all sources.")

    if settings.get('password'):
        print(f"Using provided password: {settings.get('password')}")
        settingsStr+=f"-p {settings.get('password')} "
    else:
        print("No password specified. Using default password: IWishIWasALittleBitTaller")
        settingsStr+="-p IWishIWasALittleBitTaller "

    if settings.get("gateway"):
        settingsStr+=f"-g {settings.get('gateway')} "
    else:
        print("No gateway specified. Using random generated gateway.")
    
    if settings.get("no-internet"):
        print("No internet provided.")
        settingsStr+=f"-n "
        NOINTERNET=True

    if (settings.get("nodns") and NOINTERNET==False) or (settings.get("dhcp-dns") and NOINTERNET==False):
        print("Denying use of local DNS.")
        settingsStr+=f"--no-dns "
        if settings.get("dhcp-dns"):
            print(f"Using specified DNS: {settings.get('dhcp-dns')}")
            settingsStr+=f"--dhcp-dns {settings.get('dhcp-dns')} "
        else:
            print("No custom DNS specified. Using Google DNS.")
            settingsStr+=f"--dhcp-dns 8.8.8.8 "

    if settings.get("interfaceOut"): return settingsStr,settings.get("interfaceOut")
    else: return settingsStr,"wlan0"

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




def runAP(arguments:str):
    if os.path.isdir("Logs")==False:
        os.mkdir("Logs")
    os.chdir("Logs")
    os.system(f"tmux new-session -d -s AP 'lnxrouter {arguments} 2>&1 | tee -a {datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}'.log")


if os.path.isfile(settingsFile):
    settings,interfaceOut=parseSettings(getSettings(settingsFile))
else:
    print("File not found. Using default settings.")
    settings,interfaceOut=parseSettings({})

takeDownInterface(interfaceOut)
runAP(settings)
