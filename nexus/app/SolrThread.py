import threading

class FuncThread:

    def __init__(self,,target,*args):
        
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):

        self._target(*self.args)
