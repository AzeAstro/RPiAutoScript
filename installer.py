import os



print("Starting setup")
print("Stage 1: Updating & installing packages")
os.system("sudo apt update && sudo apt install bash procps iproute2 dnsmasq iptables hostapd iw haveged -y")
