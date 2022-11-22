#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='192.168.18.88')
parser.add_argument('--port', type=int, default=88)
args = parser.parse_args()

def check_host_port(host,port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((host,port))
        print(True)
    except Exception:
        print(False)
    sk.close()

check_host_port(args.host,args.port)