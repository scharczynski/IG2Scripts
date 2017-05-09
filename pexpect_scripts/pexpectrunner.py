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
    proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/" + config)
    on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/script?run005=run"')
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


#print main('c400_limits')
#print main('c400_state')
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
    results = main("stopcount")
    assert results[0] > 980 and results[1] > 980

def test_reconnect():
    assert main('reconnect') == True

def test_reconnect_loop():
    assert main('reconnect_loop') == True

#def test_reconnect_slave():
#    assert main('reconnect_slave') == True

def test_memblock_types():
    assert main('memblock_types') == True

def test_channel_buffering():
    results = main('buffering_test')
    assert results[0] == 1000 and results[1] < 1000

def test_monitor_only_change():
    results = main('monitor_only')
    assert results[0] < 1000 and results[1] == 1000

def test_channel_limits():
    assert main('channel_limits') == [1,1,3]
    
def test_c400_init():
    results = main('c400_init')
    assert results[0] != 0 and results[1] == 1 and results[2] == 0

def test_c400_accum():
    results = main('c400_accum')
    assert results[0]+results[2] < results[1]

def test_c400_polarity():
    assert main('c400_polarity') == 4

def test_c400_limits():
    results = main('c400_limits')
    assert main[1] == 0.0, main[0] > 0.0

def test_c400_integration():
    results = main('c400_integration')
    assert results[0] >= 100 or results[1] >= 100

def test_c400_state():
    assert main('c400_state') == True