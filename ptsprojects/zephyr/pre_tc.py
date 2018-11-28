#!/usr/bin/env python

#
# auto-pts - The Bluetooth PTS Automation Framework
#
# Copyright (c) 2017, Intel Corporation.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#

import os
import sys
import atexit
import subprocess
import signal

PROFILE = None
TEST_CASE = None

RTT2PTY_PROC = None
RTT2PTY_PATH = "rtt2pty"

def cleanup():
    if RTT2PTY_PROC != None:
        RTT2PTY_PROC.terminate()

        RTT2PTY_PROC.wait()

def run_rtt2pty():
    global RTT2PTY_PROC
    RTT2PTY_PROC = subprocess.Popen([RTT2PTY_PATH, "-2", "-l", "auto-pts-tester"], shell=False)

def main():
    global PROFILE, TEST_CASE

    atexit.register(cleanup)

    PROFILE = sys.argv[1]
    TEST_CASE = sys.argv[2]

    print("#DBG# " + TEST_CASE)

    run_rtt2pty()

    while True:
        line = sys.stdin.readline()

        if line == "#close\n":
            RTT2PTY_PROC.terminate()
            RTT2PTY_PROC.wait()

            break

if __name__ == "__main__":
    main()
