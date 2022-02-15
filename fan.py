from threading import Thread, Lock
import subprocess

class Fan:

    def __init__(self):
        self.mutex = Lock ()

    def setSpeedRaw (self, speed):
        self.mutex.acquire ()
        try:
            result = subprocess.run (['./writeRegister', '53249', speed], capture_output=True)
            if result.
        finally:
            self.mutex.release ()

    def 


    