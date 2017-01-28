from blinker import signal
from functools import partial
from .page import Page

NATIVE_FUNCTIONS = (
    'addCookie',
    'clearCookies',
    'deleteCookie',
    'exit',
    'injectJs',
)


class Phantom(object):
    def __init__(self, driver):
        """
        Initialises the instance.
        :param driver: the Driver/parent
        """
        self.driver = driver
        self.on_event = signal('event')

        for f in NATIVE_FUNCTIONS:
            setattr(self, f, partial(self.invoke_function, f))

        self.driver.on_event.connect(self.process_event, 'phantom')

    def execute(self, name, *args):
        """
        Construct and execute a command.
        :param name: the command name
        :param args: the command args
        :return: the result, if any
        """
        return self.driver.execute_command({
            'scope': 'phantom',
            'name': name,
            'args': args
        })

    def create_page(self):
        """
        Create a new Page.
        :return: the Page
        """
        data = self.execute('createWebPage')
        page = Page(self.driver, data['uid'])
        return page

    def get_property(self, field):
        """
        Get a property value.
        :param field: the property name
        :return: the property value
        """
        return self.execute(
                'getProperty',
                field
        )

    def set_property(self, field, value):
        """
        Set a property value.
        :param field: the property name
        :param value: the value to set the property to
        :return: the property value
        """
        return self.execute(
                'setProperty',
                field,
                value
        )

    def invoke_asynchronous_function(self, name, *args):
        """
        Invoke an asynchronous function with the specified arguments.
        :param name: the function name
        :param args: the function args
        :return: the value(s) passed to the callback by the function, if any
        """
        return self.execute(
                'invokeAsynchronousFunction',
                name,
                args
        )

    def invoke_function(self, name, *args):
        """
        Invoke a function with the specified arguments.
        :param name: the function name
        :param args: the function args
        :return: the value returned by the function, if any
        """
        return self.execute(
                'invokeFunction',
                name,
                args
        )

    def process_event(self, sender, event):
        """
        Processes events emitted by the Driver.
        :param sender: the sender
        :param event: the event data
        """
        self.on_event.send(self, event=event)
