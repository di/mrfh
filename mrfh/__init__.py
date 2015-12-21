import fcntl
from logging import Handler
from logging.handlers import BaseRotatingHandler
import os


class MultiprocessRotatingFileHandler(BaseRotatingHandler):
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0,
                 encoding=None):
        BaseRotatingHandler.__init__(self, filename, mode, encoding)
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        head, tail = os.path.split(filename)
        self.stream_lock = open("{}/.{}.lock".format(head, tail), "w")

    def _openFile(self, mode):
        self.stream = open(self.baseFilename, mode)

    def acquire(self):
        Handler.acquire(self)
        fcntl.flock(self.stream_lock, fcntl.LOCK_EX)
        if self.stream.closed:
            self._openFile(self.mode)

    def release(self):
        if not self.stream.closed:
            self.stream.flush()
        if not self.stream_lock.closed:
            fcntl.flock(self.stream_lock, fcntl.LOCK_UN)
        Handler.release(self)

    def close(self):
        if not self.stream.closed:
            self.stream.flush()
            self.stream.close()
        if not self.stream_lock.closed:
            self.stream_lock.close()
        Handler.close(self)

    def flush(self):
        pass

    def doRollover(self):
        self.stream.close()
        if self.backupCount <= 0:
            self._openFile(self.mode)
            return
        try:
            tmpname = "{}.rot.{}".format(self.baseFilename, os.getpid())
            os.rename(self.baseFilename, tmpname)
            for i in range(self.backupCount - 1, 0, -1):
                sfn = "%s.%d" % (self.baseFilename, i)
                dfn = "%s.%d" % (self.baseFilename, i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.baseFilename + ".1"
            if os.path.exists(dfn):
                os.remove(dfn)
            os.rename(tmpname, dfn)
        finally:
            self._openFile(self.mode)

    def shouldRollover(self, record):
        def _shouldRollover():
            if self.maxBytes > 0:
                if self.stream.tell() >= self.maxBytes:
                    return True
            return False

        if _shouldRollover():
            self.stream.close()
            self._openFile(self.mode)
            return _shouldRollover()
        return False
