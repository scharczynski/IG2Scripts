import subprocess
import re
import epics
import pexpect



def prepare(proc):
    #(output, err) = proc.communicate()
    proc.expect('\[EXCEPTION[^:]*exists')
    #proc.expect(pexpect.EOF)
    error = proc.after
    before = proc.before
    #print "before " + before
    print " after "+ error
    #for line in output.splitlines():
    #    if "EXCEPTION" in line:
    #        error = line
    #if not line:
    #    print "there is no exception"
    #    return "0"
    expr = re.compile('\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}:\d{3}')
    clean = re.sub(expr, '', error).lstrip()
    return clean

def test(proc):
    message = prepare(proc)
    return message
