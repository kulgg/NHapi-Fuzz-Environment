import subprocess
from threading import Thread

class RunProcess(Thread):
    def __init__(self, cmd, input, timeout):
        Thread.__init__(self)
        self.cmd = cmd
        self.input = input
        self.timeout = timeout

    def run(self):
        self.p = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.p.stdin.write(self.input)
        self.out = self.p.communicate()[0]
        self.err = self.p.communicate()[1]
        self.p.stdin.close()
        self.p.wait()

    def Run(self):
        """
            Starts subprocess with given input command
            Returns ifTimeoutWasTriggered, stdout, stderr
        """
        self.start()
        self.join(self.timeout)
        if self.is_alive():
            self.p.terminate()
            self.join()
            return True, self.out, self.err
        return False, self.out, self.err