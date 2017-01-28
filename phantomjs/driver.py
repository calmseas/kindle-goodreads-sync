from blinker import signal
from os import path
from urllib.request import Request, urlopen
import json
import subprocess
import threading

DRIVER = path.join(path.dirname(path.realpath(__file__)), 'driver.js')


class Driver(object):
    def __init__(self, engine, port):
        """
        Initialises the instance.
        :param engine: the PhantomJS executable
        :param port: the port to listen on
        """
        self.engine = engine
        self.port = port
        self.driver = None
        self.booted = threading.Event()
        self.killed = threading.Event()
        self.on_stderr = signal('stderr')
        self.on_stdout = signal('stdout')
        self.on_event = signal('event')
        self.stderr_thread = None
        self.stdout_thread = None

    def execute_command(self, command):
        """
        Execute a command.
        :param command: the command
        :return: the result, if any
        """
        data = self.post_json(command).read().decode('utf8')
        if data:
            return json.loads(data)
        return None

    def post_json(self, data):
        """
        Post JSON data to the Driver server.
        :param data: a serializable object
        :return: the response
        """
        request = Request('http://127.0.0.1:%i' % self.port, data=json.dumps(data).encode('utf8'),
                          headers={'Content-Type': 'application/json'})
        return urlopen(request)

    def process_stderr(self):
        """
        Process the stderr stream, line by line.
        """
        while not self.killed.is_set():
            buf = self.driver.stderr.readline().decode('utf8')
            if buf is None:
                continue
            self.on_stderr.send(self, line=buf)

    def process_stdout(self):
        """
        Process the stdout stream, line by line.
        """
        while not self.killed.is_set():
            buf = self.driver.stdout.readline().decode('utf8')
            if buf is None:
                continue
            try:
                data = json.loads(buf)
            except ValueError:
                pass
            else:
                if self.booted.is_set():
                    if 'event' in data:
                        event = data['event']
                        self.on_event.send(event['scope'], event=event)
                elif 'listening' in data:
                    if data['listening']:
                        self.booted.set()
                    else:
                        self.kill()
            self.on_stdout.send(self, line=buf)

    def start(self, parameters=()):
        """
        Start the Driver.
        :param parameters: the parameters to pass to PhantomJS
        """
        command = (self.engine,) + parameters + (DRIVER, str(self.port),)
        self.driver = subprocess.Popen(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        self.stderr_thread = threading.Thread(target=self.process_stderr)
        self.stderr_thread.daemon = True
        self.stderr_thread.start()

        self.stdout_thread = threading.Thread(target=self.process_stdout)
        self.stdout_thread.daemon = True
        self.stdout_thread.start()

    def kill(self):
        """
        Kill the Driver.
        """
        self.killed.set()
        self.driver.terminate()

    def wait_for_ready(self, timeout=None):
        """
        Blocks the thread until the Driver is ready, or until the optional timeout occurs.
        :param timeout: the timeout in seconds
        :return: True unless the operation times out
        """
        return self.booted.wait(timeout)
