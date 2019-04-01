from selenium import webdriver


def init():
    global browser
    browser = webdriver.PhantomJS(executable_path='./webdrivers/phantomjs', service_args=['--ignore-ssl-errors=true'])


def close():
    print("browser closed")
    browser.close()
