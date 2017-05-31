import pytest
import pexpect
from tests.Tester import Tester as tester
from tests.M10_Tester import M10_Tester
from tests.M40_Tester import M40_Tester
from tests.Config_Tester import Config_Tester
from tests.C400_Tester import C400_Tester

path = ig2_path + ig2_version + " " + ig2_version
power_strip_ip = ''
ig2_path = "/home/steve/workspace/ig2_medical/"
config_path = ''
ig2_version = 'ig2-2.6.7'

class Test_M10(object):
    #self.path = os.path.abspath(__file__)
   
    #path = "/home/steve/workspace/ig2_medical/ig2-2.6.7 /home/steve/workspace/ig2_medical/"
    
    def test_io(self):
        tester =  M10_Tester(path, "m10_io")
        results = tester.io()
        assert all(x==True for x in results) == True
    def test_stopcount(self):
        tester = M10_Tester(path, "m10_stopcount")
        results2 = tester.stopcount()
        assert results2[0] > 980 and results2[1] < results2[0]

class Test_M40(object):
    
    def test_io(self):
        tester = M40_Tester(path, "m40_io")
        results = tester.io()
        assert all(x==True for x in results) == True
    
    def test_stopcount(self):
        tester = M40_Tester(path, "m40_stopcount")
        results2 = tester.stopcount()
        assert results2[0] > 980 and results2[1] < results2[0]

class Test_Config(object):
    
    def test_bad_defaults(self):
        tester = Config_Tester(path, "config_bad_defaults")
        results = tester.bad_defaults()
        assert results ==  "[EXCEPTION] Failed to parse given string"

    def test_broken_xml(self):
        tester = Config_Tester(path, "config_broken_xml")
        results = tester.broken_xml()
        assert results == "[EXCEPTION] Error parsing XML file"
    
    def test_config_buffering(self):
        testerA = Config_Tester(path, "config_buffering")
        resultsA = testerA.buffering()
        testerB = Config_Tester(path, "config_buffering_low")
        resultsB = testerB.buffering_low()
        assert resultsA[0] == 1000 and resultsA[1] < 1000 and resultsB > resultsA[1]

    def test_channel_limits(self):
        tester = Config_Tester(path, "config_channel_limits")
        results = tester.channel_limits()
        assert results == [1, 1, 3]

    def test_channel_scaling(self):
        tester = Config_Tester(path, "config_channel_scaling")
        results = tester.channel_scaling()
        assert results == True

    def test_defaults(self):
        tester = Config_Tester(path, "config_defaults")
        results = tester.defaults()
        assert results = (25, 5.0, 88)

    def test_monitor_only_change(self):
        tester = Config_Tester(path, "config_monitor_only")
        results = tester.monitor_only()
        assert results[0] < 1000 and results[1] == 1000
    
    def test_same_name(self):
        tester = Config_Tester(path, "config_samename")
        results = tester.same_name()
        assert results == "[EXCEPTION] [ERROR] Could not add channel with the name 'c_name', already exists"

    def test_same_wire(self):
        tester = Config_Tester(path, "config_samewire")
        results = tester.same_wire()
        assert results ==  (65.0, 65.0)

class Test_C400(object):
    

    

    ###########TESTS##############
# def test_base():
#     assert main('base') == (1.0, 45.0)

# def test_config_samename():
#     assert main('config_samename') == "[EXCEPTION] [ERROR] Could not add channel with the name 'c_name', already exists"

# def test_config_samewire():
#     assert main('config_samewire') == (65.0, 65.0)

# def test_broken():
#     assert main('broken') == "[EXCEPTION] Error parsing XML file"

# def test_config_defaults():
#     assert main('config_defaults') == (25, 5.0, 88)

# def test_config_bad_defaults():
#     assert main('config_bad_defaults') ==  "[EXCEPTION] Failed to parse given string"

# def test_config_buffering():
#     results = main('config_buffering')
#     results2 = main('config_buffering_low')
#     assert results[0] == 1000 and results[1] < 1000 and results2 > results[1]

# def test_config_monitor_only_change():
#     results = main('config_monitor_only')
#     assert results[0] < 1000 and results[1] == 1000

# def test_config_channel_limits():
#     assert main('config_channel_limits') == [1,1,3]

# def test_config_scaling():
#     assert main('config_channel_scaling') == True

# def test_m10_io():
#     results = main('m10_io')
#     assert all(x==True for x in results)

# def test_m10_stopcount():
#     results = main("m10_stopcount")
#     assert results[0] > 980 and results[1] < results[0]

# def test_reconnect():
#     assert main('reconnect') == True

# def test_reconnect_loop():
#    assert main('reconnect_loop') == True

# def test_reconnect_slave():
#    assert main('reconnect_slave') == True

# def test_memblock_types():
#     assert main('memblock_types') == True

# def test_c400_buffering():
#     results = main('c400_buffering')
#     assert results[0] == 1000 and results[1] == 500

# def test_c400_startstop():
#     results = main('c400_startstop')
#     assert results[0] < 510 and results[1] == 1 and results[2] == 0

# def test_c400_accum():
#     results = main('c400_accum')
#     assert results[0]+results[2] < results[1]

# def test_c400_polarity():
#     assert main('c400_polarity') == 4

# def test_c400_limits():
#     results = main('c400_limits')
#     assert results[1] == 0.0, results[0] > 0.0

# def test_c400_integration():
#     results = main('c400_integration')
#     assert results[0] >= 100 or results[1] >= 100

# def test_c400_state():
#     results = main('c400_state')
#     print results
#     assert all(x != None for x in results) == True

# def test_c400_in_params():
#     assert main('c400_input') == True

# def test_c400_burst():
#     results = main('c400_burst')
#     assert results[0] < results[1]

# def test_c400_pulse():
#     assert main('c400_pulse') == [10000, 100, 1, 1, 1, 1]


# def test_interface_version():
#     assert main('interface_version') == 'EPICS ENVIRONMENT 2_6_7 ENABLED'

# def test_interface_channel_names():
#     assert all(x == True for x in main('interface_channel_names')) == True

# def test_interface_disconnected_devices():
#     assert main('interface_disconnected_devices') == {'test1': 1, 'test2': 1}

# def test_c400_trigger():
#     assert main('c400_trig_2') == True

# def test_f460_trigger():
#     assert main('f460_trigger') == True

# def test_f460_burst():
    
#     assert main('f460_burst') == 100

# def test_f460_startstop():
#     assert main('f460_startstop') < 3030    

# def test_f460_buffer():
#     assert main('f460_buffer') == 1000

# def test_m40_io():
#     results = main('m40_io')
#     assert all(x==True for x in results)

# def test_m40_stopcount():
#     results = main('m40_stopcount')
#     assert results[0] > 980 and results[1] < results[0]