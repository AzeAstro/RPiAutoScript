#!/usr/bin/python3
import os,shutil


if os.geteuid()!=0:
    print("You need to run this script as root.")
    exit(1)
print("Starting setup")
print("Stage 1: Updating & installing packages")
os.system("sudo apt update && sudo apt install bash procps iproute2 dnsmasq iptables hostapd iw haveged tmux wget cron -y")
os.system("pip3 install psutil")
print("Stage 2: Installing lnxrouter")
os.system("wget https://raw.githubusercontent.com/garywill/linux-router/master/lnxrouter && chmod +x lnxrouter && cp lnxrouter /usr/bin")
print("Stage 3: Setting up crontab")
with open("/var/spool/cron/crontabs/root","+a") as f:
    f.write("\n@reboot sh /root/main.sh")
print("Stage 4: Copying scripts")
shutil.copy("AP.py","/root/")
shutil.copy("main.sh","/root/")
print("Stage 5: \nInstallation is ended. Usually, at the end, I say 'You are happy to go' but I know that if you are here, you are not happy. And you never will.\n\nWe all never will. But, all we can do is at relieve each others' pain. Maybe this time I could help you a bit. But now, it is your turn to help someone else. Good luck.")