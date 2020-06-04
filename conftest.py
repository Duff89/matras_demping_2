from selenium import webdriver
import pytest


@pytest.fixture
def browser():

    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver




