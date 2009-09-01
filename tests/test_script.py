#!/usr/bin/env python

import optparse
import supay
from time import sleep
import subprocess
import os

pid_directory = os.getcwd()
daemon = supay.Daemon(name='testScript', pid_dir=pid_directory)

def run():
    daemon.start()
    while True:
        sleep(5)

def stop():
    daemon.stop()

def spawn():
    daemon.spawn_child()
    sleep(10)

def status():
    daemon.status()

def main():
    p = optparse.OptionParser()
    options, arguments = p.parse_args()

    if arguments[0] == 'start':
        run()

    if arguments[0] == 'stop':
        stop()

    if arguments[0] == 'spawn':
        spawn()
        
    if arguments[0] == 'status':
        status()

if __name__ == '__main__':
    main()
