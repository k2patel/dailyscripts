#!/usr/bin/env python3

import psutil
import argparse
import itertools, os, augeas

# Ref: https://fasterdata.es.net/host-tuning/linux/

# Global variables
nvalue = ["net.core.rmem_max", "net.core.wmem_max", "net.ipv4.tcp_rmem", "net.ipv4.tcp_wmem", "net.ipv4.tcp_congestion_control", "net.ipv4.tcp_mtu_probing", "net.core.default_qdisc"]

#   For a host with a 10G NIC optimized for network paths up to 200ms RTT, and for friendliness to single and parallel stream tools, or a 40G NIC up on paths up to 50ms RTT:
v4000050 = ["134217728", "134217728", "4096 87380 67108864", "4096 65536 67108864", "htcp", "1", "fq"]

v40000100 = ["134217728", "134217728", "4096 87380 67108864", "4096 65536 67108864", "htcp", "1", "fq"]
v10000200 = ["134217728", "134217728", "4096 87380 67108864", "4096 65536 67108864", "htcp", "1", "fq"]

# For a host with a 10G NIC, optimized for network paths up to 100ms RTT, and for friendlyness to single and parallel stream tools, add this to /etc/sysctl.conf
v10000100 = ["67108864", "67108864", "4096 87380 33554432", "4096 65536 33554432", "htcp", "1", "fq"]
v1000100 = ["229376", "229376", "4096 131072 8388608", "4096 131072 8388608", "htcp", "1", "fq"]

# Linux supports pluggable congestion control algorithms. To get a list of congestion control algorithms that are available in your kernel (kernal  2.6.20+), run:

# sysctl net.ipv4.tcp_available_congestion_control
# cubic is usually the default in most linux distribution, but we have found htcp usually works better. You might also want to try BBR if its available on your system.

# To set the default congestion control algorithm, do:

# sysctl -w net.ipv4.tcp_congestion_control=htcp

def main():
    parser = argparse.ArgumentParser(prog='tunenetwork')
    parser.add_argument('-i', '--interface', dest='ifname', type=str, help='Interface name to tune', required=True)
    parser.add_argument('-r', '--rtt', dest='rtt', type=int, help='Round trip time', required=True)
    args = parser.parse_args()
    status = tunenetwork(args.ifname, args.rtt)
    return status

def get_speed(ifname):
    for id, net in psutil.net_if_stats().items():
        if id == ifname and net.isup:
            return net.speed

def tunenetwork(ifname, rtt):
    speed = get_speed(ifname)
    for (svar, sval) in zip(nvalue, eval('v' + str(speed) + str(rtt))):
        aug = augeas.Augeas()
        aug.set('/files/etc/sysctl.d/tuner.conf/' + svar, str(sval))
        aug.save()
    try:
        os.system('/usr/bin/systemctl restart systemd-sysctl')
        return True
    except:
        return False

if __name__ == "__main__":
    main()