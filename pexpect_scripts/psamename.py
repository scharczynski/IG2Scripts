import subprocess
import re
import epics
import pexpect



def prepare(proc):

    proc.expect('\[EXCEPTION[^:]*exists')

    error = proc.after
    before = proc.before
 
    #print " after "+ error

    expr = re.compile('\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}:\d{3}')
    clean = re.sub(expr, '', error).lstrip()
    return clean

def test(proc):
    message = prepare(proc)
    return message
