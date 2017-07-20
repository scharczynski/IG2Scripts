import pexpect
import epics
import hypothesis.strategies as st

def valid_analog_outs(size):
    return st.lists(st.floats(min_value=0.001, max_value=10.00), min_size=size, max_size=size)

def valid_digital_outs(size):
    return st.lists(st.integers(min_value=0, max_value=1), min_size=size, max_size=size)

def valid_stopcount():
    return st.integers(min_value=10, max_value=400)

def valid_memblock_a_o():
    return st.floats(min_value=-400, max_value=400)
    
