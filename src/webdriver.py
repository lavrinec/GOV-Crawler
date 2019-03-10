from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")


def init():
    global driver
    driver = webdriver.Chrome(executable_path='./webdrivers/chromedriver-2-46', chrome_options=chrome_options)


def close():
    driver.close()
