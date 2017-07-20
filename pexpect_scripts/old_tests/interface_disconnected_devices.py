import epics
import subprocess
import pexpect
import re

devices = {'loop1': 0, 'loop2':0}
#names = ('test1', 'test2')

def test(proc):
    for x in devices.keys():
        connect = proc.expect(['Error: could not connect to.*', pexpect.TIMEOUT, pexpect.EOF], timeout=10)
        print proc.after
        print proc.before
        if connect == 0:
            last = proc.after.rsplit(None, 1)[-1]
            #print last
            if last in devices.keys():
                devices[last] = 1

    
    return devices
    #while True:
    #    line = proc.stdout.readline()
    #    if not line:
    #        print "end of output"
    #        break
    #    else:
    #        if "Error" in line:
    #            for i in devices.keys():
    #                if i in line:
    #                    devices[i] = 1
    #    if all(x==1 for x in devices.values()):
    #        return devices
