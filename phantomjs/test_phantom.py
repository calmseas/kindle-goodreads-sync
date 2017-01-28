from .page import Page
from .phantom import Phantom
from .driver import Driver
import pytest


@pytest.fixture()
def phantom(request):
    driver = Driver(engine='phantomjs', port=3000)
    driver.start()
    driver.wait_for_ready()
    phantom = Phantom(driver=driver)
    request.addfinalizer(driver.kill)
    return phantom


def test_create_page(phantom):
    value = phantom.create_page()
    assert isinstance(value, Page)


def test_get_property(phantom):
    value = phantom.get_property('cookiesEnabled')
    assert value is True


def test_set_property(phantom):
    value = phantom.set_property('cookiesEnabled', False)
    assert value is False


def test_invoke_function(phantom):
    value = phantom.deleteCookie('Nonexistent-Cookie')
    assert value is False
