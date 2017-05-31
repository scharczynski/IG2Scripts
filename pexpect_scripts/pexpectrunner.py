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

#spawns the pexpect process 
def initialize(config):
    proc = pexpect.spawn("/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/" + config)

    #runs script to make sure devices are on when script begins
    on = pexpect.spawn('curl "http://admin:1234@192.168.100.36/script?run005=run"')
    return proc

#unused
def kill_ig2(proc):
    if proc.pid is None:
        pass
    else:
        try:
            os.kill(proc.pid, signal.SIGTERM)
        except OSError:
            print "already dead?"

#dynamically imports the test script
def run(test, proc):
    module = importlib.import_module(str(test))
    return module.test(proc)

#feeds the correct xml to IG2, then runs the test
def main(name):
    proc = initialize(name+'.xml')
    #while caget('status') != 0:
    #    time.sleep(0.1)
    outcome = run(name, proc)
    #kill_ig2(proc)
    return outcome


#print main('m10_io')
#print main('config_buffering')
#print main('buffering_test')
#print main('m40_stopcount')
#print main('monitor_only')
#print main('c400_limits')
    ###########TESTS##############
def test_base():
    assert main('base') == (1.0, 45.0)

def test_config_samename():
    assert main('config_samename') == "[EXCEPTION] [ERROR] Could not add channel with the name 'c_name', already exists"

def test_config_samewire():
    assert main('config_samewire') == (65.0, 65.0)

def test_broken():
    assert main('broken') == "[EXCEPTION] Error parsing XML file"

def test_config_defaults():
    assert main('config_defaults') == (25, 5.0, 88)

def test_config_bad_defaults():
    assert main('config_bad_defaults') ==  "[EXCEPTION] Failed to parse given string"

def test_config_buffering():
    results = main('config_buffering')
    results2 = main('config_buffering_low')
    assert results[0] == 1000 and results[1] < 1000 and results2 > results[1]

def test_config_monitor_only_change():
    results = main('config_monitor_only')
    assert results[0] < 1000 and results[1] == 1000

def test_config_channel_limits():
    assert main('config_channel_limits') == [1,1,3]

def test_config_scaling():
    assert main('config_channel_scaling') == True

def test_m10_io():
    results = main('m10_io')
    assert all(x==True for x in results)

def test_m10_stopcount():
    results = main("m10_stopcount")
    assert results[0] > 980 and results[1] < results[0]

def test_reconnect():
    assert main('reconnect') == True

def test_reconnect_loop():
   assert main('reconnect_loop') == True

def test_reconnect_slave():
   assert main('reconnect_slave') == True

def test_memblock_types():
    assert main('memblock_types') == True

def test_c400_buffering():
    results = main('c400_buffering')
    assert results[0] == 1000 and results[1] == 500

def test_c400_startstop():
    results = main('c400_startstop')
    assert results[0] < 510 and results[1] == 1 and results[2] == 0

def test_c400_accum():
    results = main('c400_accum')
    assert results[0]+results[2] < results[1]

def test_c400_polarity():
    assert main('c400_polarity') == 4

def test_c400_limits():
    results = main('c400_limits')
    assert results[1] == 0.0, results[0] > 0.0

def test_c400_integration():
    results = main('c400_integration')
    assert results[0] >= 100 or results[1] >= 100

def test_c400_state():
    results = main('c400_state')
    print results
    assert all(x != None for x in results) == True

def test_c400_in_params():
    assert main('c400_input') == True

def test_c400_burst():
    results = main('c400_burst')
    assert results[0] < results[1]

def test_c400_pulse():
    assert main('c400_pulse') == [10000, 100, 1, 1, 1, 1]


def test_interface_version():
    assert main('interface_version') == 'EPICS ENVIRONMENT 2_6_7 ENABLED'

def test_interface_channel_names():
    assert all(x == True for x in main('interface_channel_names')) == True

def test_interface_disconnected_devices():
    assert main('interface_disconnected_devices') == {'test1': 1, 'test2': 1}

def test_c400_trigger():
    assert main('c400_trig_2') == True

def test_f460_trigger():
    assert main('f460_trigger') == True

def test_f460_burst():
    
    assert main('f460_burst') == 100

def test_f460_startstop():
    assert main('f460_startstop') < 3030    

def test_f460_buffer():
    assert main('f460_buffer') == 1000

def test_m40_io():
    results = main('m40_io')
    assert all(x==True for x in results)

def test_m40_stopcount():
    results = main('m40_stopcount')
    assert results[0] > 980 and results[1] < results[0]