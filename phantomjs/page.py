from blinker import signal
from functools import partial

NATIVE_ASYNCHRONOUS_FUNCTIONS = (
    'includeJs',
    'open',
)

NATIVE_FUNCTIONS = (
    'addCookie',
    'childFramesCount',
    'childFramesName',
    'clearCookies',
    'close',
    'currentFrameName',
    'deleteCookie',
    'evaluateJavaScript',
    'getPage',
    'go',
    'goBack',
    'goForward',
    'injectJs',
    'openUrl',
    'release',
    'reload',
    'render',
    'renderBase64',
    'sendEvent',
    'setContent',
    'stop',
    'switchToChildFrame',
    'switchToFocusedFrame',
    'switchToFrame',
    'switchToMainFrame',
    'switchToParentFrame',
    'uploadFile',
)


class Page(object):
    def __init__(self, driver, uid):
        """
        Initialises the instance.
        :param driver: the Driver/parent
        :param uid: the Page's unique identifier
        """
        self.driver = driver
        self.uid = uid
        self.on_event = signal('event')

        for f in NATIVE_ASYNCHRONOUS_FUNCTIONS:
            setattr(self, f, partial(self.invoke_asynchronous_function, f))

        for f in NATIVE_FUNCTIONS:
            setattr(self, f, partial(self.invoke_function, f))

        self.driver.on_event.connect(self.process_event, sender=self.uid)

    def execute(self, name, *args):
        """
        Construct and execute a command.
        :param name: the command name
        :param args: the command args
        :return: the result, if any
        """
        return self.driver.execute_command({
            'scope': self.uid,
            'name': name,
            'args': args
        })

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

    def get_setting(self, field):
        """
        Get a setting.
        :param field: the property name
        :return: the property value
        """
        return self.execute(
                'getSetting',
                field
        )

    def set_setting(self, field, value):
        """
        Set a setting.
        :param field: the property name
        :param value: the property value
        :return: the property value
        """
        return self.execute(
                'setSetting',
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
