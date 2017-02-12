# -*- coding:utf-8 -*-

import socket
import platform
import traceback


def get_current_ip():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127.") and platform.system()=="Linux":
            import fcntl, struct
            interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0", "ath0", "ath1", "ppp0"]
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for ifname in interfaces:
                try:
                    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
                except IOError:
                    pass
        return ip
    except:
        print 'get_current_ip failed, error: %s' % traceback.format_exc()
        return ''
