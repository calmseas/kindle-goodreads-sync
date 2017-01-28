from .phantom import Phantom
from .driver import Driver
import pytest


@pytest.fixture()
def page(request):
    driver = Driver(engine='phantomjs', port=3000)
    driver.start()
    driver.wait_for_ready()
    phantom = Phantom(driver=driver)
    page = phantom.create_page()
    request.addfinalizer(driver.kill)
    return page


def test_get_property(page):
    value = page.get_property('zoomFactor')
    assert value == 1


def test_set_property(page):
    value = page.set_property('zoomFactor', 0.5)
    assert value == 0.5


def test_get_setting(page):
    value = page.get_setting('javascriptEnabled')
    assert value is True


def test_set_setting(page):
    value = page.set_setting('javascriptEnabled', False)
    assert value is False


def test_invoke_asynchronous_function(page):
    value = page.open('http://phantomjs.org/')
    assert value in ('fail', 'success',)


def test_invoke_function(page):
    value = page.evaluateJavaScript('function(){return "Hello, world!";}')
    assert value == 'Hello, world!'
