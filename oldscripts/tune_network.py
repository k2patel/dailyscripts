#!/usr/bin/env python3
import os
import argparse, itertools, sys, subprocess

# Ref: https://fasterdata.es.net/host-tuning/linux/

# Global variables
nvalue = ['net.core.rmem_max', 'net.core.wmem_max', 'net.ipv4.tcp_rmem', 'net.ipv4.tcp_wmem', 'net.ipv4.tcp_congestion_control', 'net.ipv4.tcp_mtu_probing', 'net.core.default_qdisc']
#   For a host with a 10G NIC optimized for network paths up to 200ms RTT, and for friendliness to single and parallel stream tools, or a 40G NIC up on paths up to 50ms RTT:
v4000050 = ['134217728', '134217728', '4096 87380 67108864', '4096 65536 67108864', 'htcp', '1', 'fq']
v40000100 = ['134217728', '134217728', '4096 87380 67108864', '4096 65536 67108864', 'htcp', '1', 'fq']
v10000200 = ['134217728', '134217728', '4096 87380 67108864', '4096 65536 67108864', 'htcp', '1', 'fq']
# For a host with a 10G NIC, optimized for network paths up to 100ms RTT, and for friendlyness to single and parallel stream tools, add this to /etc/sysctl.conf
v10000100 = ['67108864', '67108864', '4096 87380 33554432', '4096 65536 33554432', 'htcp', '1', 'fq']

# Linux supports pluggable congestion control algorithms. To get a list of congestion control algorithms that are available in your kernel (kernal  2.6.20+), run:

# sysctl net.ipv4.tcp_available_congestion_control
# cubic is usually the default in most linux distribution, but we have found htcp usually works better. You might also want to try BBR if its available on your system. 

# To set the default congestion control algorithm, do:

# sysctl -w net.ipv4.tcp_congestion_control=htcp

def check_speed(speed_information):
    try:
        with open('/sys/class/net/' + args.interface + '/speed') as f:
            return f.read().strip("\n")
    except IOError:
        return "No interface found"

def setnewval(name_array):
    tempary = eval(name_array)
    for (var, val) in zip(nvalue, tempary):
        p = subprocess.check_output(["/usr/sbin/sysctl", '-w', var+'='+val]).decode("utf-8")
    return True

def checkoldval(name_array):
    tempary = eval(name_array)
    for (var, val) in zip(nvalue, tempary):
        p = subprocess.check_output(["/usr/sbin/sysctl", var]).decode("utf-8")
        if int(p.split('=')[1].strip()) != val:
            return False
    else:
        return True
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Tune network for speed defined")
    parser.add_argument("-i", "--interface", help="Please provide interface need to be targated")
    parser.add_argument("-rtt", "--roundtriptime", help="Please provide round trip time for network path targated", default='100')
    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    speed = check_speed(args.interface)
    if speed == 'No interface found':
        print('No interface found')
    elif int(speed) >= 40000:
        print('speed of network is 40G or more')
    elif int(speed) == 10000:
        if not checkoldval('v'+speed+args.roundtriptime):
            if setnewval('v'+speed+args.roundtriptime):
                print('done')
            else:
                print('failed')
    elif int(speed) == 1000:
        print('OS Default should works just fine')
    else:
        print('provided speed size not known')
