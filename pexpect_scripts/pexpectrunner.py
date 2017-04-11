import subprocess
import re
import epics
import os
import signal
import time
import importlib
import pytest
from epics import caput, caget, PV, ca, pv
import pexpect


def initialize(config):
    proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 config/" + config)
    return proc

def kill_ig2(proc):
    if proc.pid is None:
        pass
    else:
        try:
            os.kill(proc.pid, signal.SIGTERM)
        except OSError:
            print "already dead?"

def run(test, proc):
    module = importlib.import_module("p"+test)
    return module.test(proc)

def main(name):
    proc = initialize(name+'.xml')
    #while caget('status') != 0:
    #    time.sleep(0.1)
    outcome = run(name, proc)
    #kill_ig2(proc)
    return outcome

print main('reconnect')
    ###########TESTS##############
def test_base():
    assert main('base') == (1.0, 45.0)

def test_samename():
    assert main('samename') == "[EXCEPTION] [ERROR] Could not add channel with the name 'c_name', already exists"

def test_samewire():
    assert main('samewire') == (65.0, 65.0)

def test_broken():
    assert main('broken') == "[EXCEPTION] Error parsing XML file"

def test_disconnected():
    assert main('disconnected_device') == {'test1': 1, 'test2': 1}

def test_defaults():
    assert main('defaults') == (25, 5.0, 88)

def test_badDefault():
    assert main('badDefault') ==  "[EXCEPTION] Failed to parse given string"

def test_m10():
    assert main('m10test') == (1,1,1,1, 5.0, 9.0)

def test_stopcount():
    assert main('stopcount') == (99,99)

def test_reconnect():
    assert main('reconnect') == True

def test_reconnect_loop():
    assert main('reconnect_loop') == True

def test_reconnect_slave():
    assert main('reconnect_slave') == True