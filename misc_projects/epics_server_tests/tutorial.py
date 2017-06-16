from pcaspy import SimpleServer, Driver

prefix = ''
pvdb = {
    'stop_trigger_source' : {
        'prec' : 3,
    },
    'acquisition_mode' : {
        'prec' : 3,
    },
    'start_trigger_source' : {
        'prec' : 3,
    },
    'pause_trigger_source' : {
        'prec' : 3,
    },
    'status' : {
        'value' : 1,
    },

    'acquisition_mode' : {
        'value' : 0,
    },
}

class myDriver(Driver):
    def  __init__(self):
        super(myDriver, self).__init__()

if __name__ == '__main__':
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()

    # process CA transactions
    while True:
        server.process(0.1)