import subprocess


DEPENDENCIES=["bash","procps","iproute2","dnsmasq","iptables","hostapd","iw","haveged"]
installedPackages=[]
notInstalledPackages=[]


rawAptOutput=subprocess.getoutput("apt list").split("\n")
rawAptOutput=rawAptOutput[4:]


for package in rawAptOutput:
    if "installed" in package:
        installedPackages.append(package.split("/")[0])

for dependency in DEPENDENCIES:
    if dependency not in installedPackages:
        notInstalledPackages.append(dependency)


print("Starting setup")