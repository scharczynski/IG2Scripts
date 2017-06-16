import pexpect
from epics import caget, caput, PV, ca, get_pv, pv, poll, _PVmonitors_
import time
from util import epics_util as util
from tests.Tester import Tester
import epics
import random

class PSU_Tester(Tester):

    def __init__(self, path, test_name):
        self.path = path + str(test_name)
        Tester.__init__(self, self.path)
        print self.path
        

    def set_command_voltage(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        print self.proc.after
        print self.proc.before
        if connect == 2:

            command_v = PV('c_psu_control_voltage')
            value = random.random()*1000
            command_v.put(value)
            poll(evt=1.0, iot=1.0)
            command = command_v.get()
            print command_v.info
            print command
            print command_v.get()
            #teardown
            #command_v.disconnect()
            #util.blowout_pvs()
            # epics.ca.clear_channel(command_v.chid)
            # ctx = epics.ca.current_context()
            # pvs = []
            # for x in epics.ca._cache[ctx]:
            #     pvs.append(x)
            # for pv in pvs:
            #     epics.ca._cache[ctx].pop(pv)
            #print epics.ca._cache[ctx]
            #epics.ca._cache[ctx].pop('c_psu_control_voltage')

            return command, value
        else:
            return -1

    def set_command_current(self):
        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect == 2:

            command_i = PV('c_psu_control_current')
            value = random.random()
            command_i.put(value)
            poll(evt=1.0, iot=1.0)

            return command_i.get(), value
        else:
            return -1

    def get_readbacks(self):

        connect = self.proc.expect(
            [pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
        if connect == 2:

            
            #enable = PV('c_psu_enable')
            resistance = PV('c_psu_resistance')
            readback_current = PV('r_psu_current')
            readback_voltage = PV('r_psu_voltage')
        
            # setpoint_current = PV('analog_in_current_setpoint')
            # setpoint_voltage = PV('analog_in_voltage_setpoint')
            command_v = PV('c_psu_control_voltage')
            poll(evt=1.0, iot=1.0)
            command_v.put(400)
            
            poll(evt=1.0, iot=1.0)
            change = self.proc.expect([pexpect.TIMEOUT, pexpect.EOF, 'success'], timeout=5)
            print self.proc.before
            print self.proc.after
            print command_v.info
            print resistance.info
            print command_v.get()

            r_curr = readback_current.get()
            r_volt = readback_voltage.get()
            # set_curr = setpoint_current.get()
            # set_volt = setpoint_voltage.get()

            intended = r_curr * resistance.get()

            return r_curr, r_volt, intended, command_v.get()
        else:
            return -1

    