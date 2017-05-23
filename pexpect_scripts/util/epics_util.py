from epics import caget, caput, poll
import time


def pv_check(pvname, value):
    poll(evt=1.e-5, iot=0.01)
    if caget(pvname) == value:
        return True
    else:
        t0 = time.time()
        while caget(pvname) != value:
            poll(evt=1.e-5, iot=0.01)
       
            caput(pvname, value)
            current = caget(pvname)
            
            if time.time() - t0 > 5:
                #raise ValueError("setting " + pvname + " timed out, set value was " + str(value) + " actual value was: " + str(caget(pvname)))
                print ("setting " + pvname + " timed out, set value was " + str(value) + " actual value was: " + str(current))
                return False
            else:
                pass
        return True

def put_check(pvname, value):
    caput(pvname, value)
    return pv_check(pvname, value)

def check_fuzzy(pvname, value, envelope):
    pv_value = caget(pvname)
    under  = -1*value*envelope + value
    over = value*envelope + value

    t0 = time.time()
    while pv_value < under or pv_value > over:
        if time.time() - t0 > 10:
            raise ValueError("setting " + pvname + " timed out, value was " + str(value))
            return False
        else:
            if pv_value >= under or pv_value <= over:
                return True
    return True

def put_fuzzy(pvname, value, envelope):
    caput(pvname, value)
    return check_fuzzy(pvname, value, envelope)
        
        

