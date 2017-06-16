import pytest
import pexpect
import epics
import pytest_jira
from tests.Tester import Tester as tester
from tests.M10_Tester import M10_Tester
from tests.M40_Tester import M40_Tester
from tests.Config_Tester import Config_Tester
from tests.C400_Tester import C400_Tester
from tests.F460_Tester import F460_Tester
from tests.Interface_Tester import Interface_Tester
from tests.Memblock_Tester import Memblock_Tester
from tests.PSU_Tester import PSU_Tester
from util import epics_util as util


ig2_version = 'ig2-2.6.7'   
ig2_path = "/home/steve/workspace/nt_ig2/"
path = ig2_path + ig2_version + " " + ig2_path
power_strip_ip = ''

config_path = ''

# class Test(object):
#     ig2_version = ''   
#     ig2_path = ""
#     path = ig2_path + ig2_version + " " + config_path + ig2_path
#     power_strip_ip = ''
#     config_path = ''

@pytest.fixture()
def set_params():
    ig2_version = 'ig2-2.6.7'   
    ig2_path = "/home/steve/workspace/nt_ig2/"
    config_path = ''
    path = ig2_path + ig2_version + " " + config_path + ig2_path
    power_strip_ip = ''
    
    return path

@pytest.fixture()
def use_server():
    path = "python /home/steve/workspace/IG2Scripts/misc_projects/epics_server_tests/tutorial.py"
    return path

class Test_M10(object):

    @pytest.mark.jira("NT-37")
    def test_io(self):
        tester =  M10_Tester(path, "m10_io.xml")
        results = tester.io()
        tester.kill_pexpect()
        assert all(x==True for x in results) == True
    def test_stopcount(self):
        tester = M10_Tester(path, "m10_stopcount.xml")
        results2 = tester.stopcount()
        tester.kill_pexpect()
        assert results2[0] >= 980 and results2[1] < results2[0]

class Test_M40(object):
    
    def test_io(self):
        tester = M40_Tester(path, "m40_io.xml")
        results = tester.io()
        tester.kill_pexpect()
        assert all(x==True for x in results) == True
    
    def test_stopcount(self):
        tester = M40_Tester(path, "m40_stopcount.xml")
        results2 = tester.stopcount()
        tester.kill_pexpect()
        assert results2[0] >= 980 and results2[1] < results2[0]

class Test_Config(object):
    
    def test_bad_defaults(self):
        tester = Config_Tester(path, "config_bad_defaults.xml")
        results = tester.bad_defaults()
        tester.kill_pexpect()
        assert results ==  "[EXCEPTION] Failed to parse given string"

    def test_broken_xml(self):
        tester = Config_Tester(path, "config_broken_xml.xml")
        results = tester.broken_xml()
        tester.kill_pexpect()
        assert results == "[EXCEPTION] Error parsing XML file"
    
    def test_config_buffering(self):
        testerA = Config_Tester(path, "config_buffering.xml")
        resultsA = testerA.buffering()
        testerA.kill_pexpect()
        testerB = Config_Tester(path, "config_buffering_low.xml")
        resultsB = testerB.buffering_low()
        testerB.kill_pexpect()
        assert resultsA[0] == 1000 and resultsA[1] < 1000 and resultsB > resultsA[1]

    def test_channel_limits(self):
        tester = Config_Tester(path, "config_channel_limits.xml")
        results = tester.channel_limits()
        tester.kill_pexpect()
        assert results == [1, 1, 3]

    def test_channel_scaling(self):
        tester = Config_Tester(path, "config_channel_scaling.xml")
        results = tester.channel_scaling()
        tester.kill_pexpect()
        assert results == True

    def test_defaults(self):
        tester = Config_Tester(path, "config_defaults.xml")
        results = tester.defaults()
        tester.kill_pexpect()
        assert results == (25, 5.0, 88)

    def test_monitor_only_change(self):
        tester = Config_Tester(path, "config_monitor_only.xml")
        results = tester.monitor_only()
        tester.kill_pexpect()
        assert results[0] < 1000 and results[1] == 1000
    
    def test_same_name(self):
        tester = Config_Tester(path, "config_samename.xml")
        results = tester.same_name()
        tester.kill_pexpect()
        assert results == "[EXCEPTION] [ERROR] Could not add channel with the name 'c_name', already exists"

    def test_same_wire(self):
        tester = Config_Tester(path, "config_samewire.xml")
        results = tester.same_wire()
        tester.kill_pexpect()
        assert results ==  (65.0, 65.0)

class Test_C400(object):
    
    def test_accumulate_mode(self):
        tester = C400_Tester(path, "c400_accum.xml")
        results = tester.accumulate_mode()
        tester.kill_pexpect()    
        assert results[0]+results[2] < results[1]

    def test_buffer_size(self):
        tester = C400_Tester(path, "c400_buffering.xml")
        results = tester.buffering()
        tester.kill_pexpect()
        assert results[0] == 1000 and results[1] == 500
    
    def test_burst_size(self):
        tester = C400_Tester(path, "c400_burst.xml")
        results = tester.burst_size()
        tester.kill_pexpect()
        assert results[0] < results[1]

    def test_io(self):
        tester = C400_Tester(path, "c400_input.xml")
        results = tester.io()
        tester.kill_pexpect()
        print results
        assert results == True
    
    def test_integration_set(self):
        tester = C400_Tester(path, "c400_integration.xml")
        results = tester.integration_set()
        tester.kill_pexpect()
        assert results[0] >= 100 or results[1] >= 100
    
    def test_discriminator_limits(self):
        tester = C400_Tester(path, "c400_limits.xml")
        results = tester.discriminator_limits()
        tester.kill_pexpect()
        print results
        assert results[1] == 0.0 and results[0] > 0.0
    
    def test_polarity_set(self):
        tester = C400_Tester(path, "c400_polarity.xml")
        results = tester.polarity()
        tester.kill_pexpect()
        assert results == 4

    def test_pulse(self):
        tester = C400_Tester(path, "c400_pulse.xml")
        results = tester.pulse()
        tester.kill_pexpect()
        assert results == [10000, 100, 1, 1, 1, 1]

    def test_init_abort(self):
        tester = C400_Tester(path, "c400_startstop.xml")
        results = tester.start_stop()
        tester.kill_pexpect()
        print results
        assert results[0] < 510 and results[1] == 1 and results[2] == 0

    def test_state(self):
        tester = C400_Tester(path, "c400_state.xml")
        results = tester.state()
        tester.kill_pexpect()
        assert all(x != None for x in results) == True

    def test_trigger_modes(self):
        tester = C400_Tester(path, "c400_trigger.xml")
        results = tester.trigger_modes()
        tester.kill_pexpect()
        assert results == True


class Test_F460(object):
    
    def test_buffer_mode(self, use_server):
        # epics_tester = F460_Tester(use_server, 'epics')
        # epics_results = epics_tester.buffer_mode()
        tester = F460_Tester(path, "f460_buffer.xml")
        results = tester.buffer_mode()
        tester.kill_pexpect()
        #epics.ca.clear_cache()
        assert results[0] == pytest.approx(500, abs=5)  and results[1] < 300

    def test_burst_size(self):
        tester = F460_Tester(path, "f460_burst.xml")
        results = tester.burst_size()
        tester.kill_pexpect()
        assert results == 2000

    def test_io(self):
        tester = F460_Tester(path, "f460_input.xml")
        results = tester.io()
        tester.kill_pexpect()
        assert all(x != None for x in results) == True

    
    def test_initiate_abort(self):
        tester = F460_Tester(path, "f460_startstop.xml")
        results = tester.initiate_abort()
        tester.kill_pexpect()
        assert results <= 1100 and results > 1

    def test_version_numbers(self):
        tester = F460_Tester(path, "f460_versions.xml")
        results = tester.version_numbers()
        tester.kill_pexpect()
        assert all(x != None for x in results) == True

    def test_set_start_trig(self):
        tester =  F460_Tester(path, "f460_versions.xml")
        results = tester.trigger_start()
        tester.kill_pexpect()
        print results
        assert all(x == True for x in results) == True
    
    def test_set_pause_trig(self):
        tester =  F460_Tester(path, "f460_versions.xml")
        results = tester.trigger_pause()
        tester.kill_pexpect()
        print results
        assert all(x == True for x in results) == True

    def test_set_stop_trig(self, use_server):
        tester =  F460_Tester(path, "f460_versions.xml")
        results = tester.trigger_stop()
        tester.kill_pexpect()
        print results
        assert all(x == True for x in results) == True

    def test_set_acquisition_modes(self):
        tester = F460_Tester(path, "f460_versions.xml")
        results = tester.acquisition_modes()
        tester.kill_pexpect()
        assert all(x == True for x in results) == True
    
    def test_set_gate_polarity(self):
        tester = F460_Tester(path, "f460_input.xml")
        results = tester.gate_polarity()
        tester.kill_pexpect()
        assert all(x == True for x in results) == True

    def test_set_input_range(self):
        tester = F460_Tester(path, "f460_input.xml")
        results = tester.input_range()
        tester.kill_pexpect()
        assert all(x == True for x in results) == True

    # def test_trigger_server(self, use_server):
    #     tester1 = F460_Tester(use_server, 'epics')
    #     results1 = tester1.trigger_stop()
    #     tester1.kill_pexpect()

    #     tester2 = F460_Tester(use_server, 'epics')
    #     results2 = tester2.trigger_pause()
    #     tester2.kill_pexpect()

    #     tester3 = F460_Tester(use_server, 'epics')
    #     results3 = tester3.trigger_start()
    #     tester3.kill_pexpect()
    #     print results1, results2, results3
    #     assert all(x == True for x in results1) == True and all(x == True for x in results2) == True and all(x == True for x in results3) == True



class Test_Interface(object):

    def test_epics_supported(self):
        tester = Interface_Tester(path, "interface_version.xml")   
        results = tester.epics_version()
        tester.kill_pexpect()
        assert results == 'EPICS ENVIRONMENT 2_6_7 ENABLED'

    def test_disconnected_device_messages(self):
        tester = Interface_Tester(path, "interface_disconnected_device.xml")
        results = tester.disconnected_devices()
        tester.kill_pexpect()
        assert all(x == 1 for x in results.values())

    def test_channel_name_propagation(self):
        tester = Interface_Tester(path, "interface_channel_names.xml")
        results = tester.channel_name_propagation()
        tester.kill_pexpect()
        assert all(x == True for x in results) == True

class Test_Memblock(object):
    
    def test_memblock_types(self):
        tester = Memblock_Tester(path, "memblock_types.xml")
        results = tester.data_types()
        tester.kill_pexpect()
        assert results == True

class Test_PSU(object):
    
    
    # ig2_version = 'ig2-2.6.7'   
    # ig2_path = "/home/steve/workspace/nt_ig2/"
    # path = ig2_path + ig2_version + " " + ig2_path

    def test_set_voltage(self, set_params):
        tester = PSU_Tester(set_params, "powersupply.xml")
        results = tester.set_command_voltage()
        tester.kill_pexpect()
        print results
        assert results[1] == pytest.approx(results[0], rel=1.0)        

    def test_set_current(self, set_params):
        tester = PSU_Tester(set_params, "powersupply.xml")
        results = tester.set_command_current()
        tester.kill_pexpect()
        assert results[1] == pytest.approx(results[0], rel=0.01)

    def test_get_readbacks(self, set_params):
        tester = PSU_Tester(set_params, "powersupply.xml")
        results = tester.get_readbacks()
        tester.kill_pexpect()
        assert all(x != 0.0 for x in results) == True

    
    

        
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
#     assert main('f460_buffer') == 1000==

# def test_m40_io():
#     results = main('m40_io')
#     assert all(x==True for x in results)

# def test_m40_stopcount():
#     results = main('m40_stopcount')
#     assert results[0] > 980 and results[1] < results[0]