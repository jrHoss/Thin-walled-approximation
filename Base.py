from datetime import datetime


class Base:
    # class properties (available only ONCE!)
    # (like a global variable)
    _log = "twp.log"  # log file name
    _counter = 0  # counts initialized object
    _nextId = 1  # initiatized ID of next object to instances

    # define the constructor
    def __init__(self, log=""):
        self._id = Base._nextId  # object id
        if log != "": Base._log = log
        # update the counter and nextId

        Base._counter += 1
        Base._nextId += 1
        Base.appendLog("instance %d created." \
                       "%d instance(s) found" \
                       % (self._id, Base._counter))

    def __del__(self):
        self.appendLog("delete instance %d." % self._id)
        Base._counter -= 1

    @classmethod
    def appendLog(cls, text):
        t = datetime.now()
        tstamp = "%2.2d.%2.2d.%2.2d| " % (t.hour, t.minute, t.second)
        textout = tstamp + text

        f = open(Base._log, "a")
        f.write(textout + "\n")
        f.close()
        print(textout)  # print to screen

    @classmethod
    def clearLogfile(cls):
        import os
        try:
            os.remove(Base._log)
        except:
            print("***WARNING: Could not delete the log file" + Base._log)

    @classmethod
    def setLogfileName(cls, text):
        Base._log = text
        Base.clearLogfile()
