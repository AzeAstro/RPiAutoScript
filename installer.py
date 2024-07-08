import os



print("Starting setup")
print("Stage 1: Updating & installing packages")
os.system("sudo apt update && sudo apt install bash procps iproute2 dnsmasq iptables hostapd iw haveged tmux wget -y")
os.system("pip3 install psutil")
print("Stage 2: Installing lnxrouter")
os.system("wget https://raw.githubusercontent.com/garywill/linux-router/master/lnxrouter && chmod +x lnxrouter && cp lnxrouter /usr/bin")
