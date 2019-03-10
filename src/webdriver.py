from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# chrome_options = Options()
# chrome_options.add_argument("--headless")


def init():
    global browser
    # browser = webdriver.Chrome(executable_path='./webdrivers/chromedriver-2-46', chrome_options=chrome_options)
    browser = webdriver.PhantomJS(executable_path='./webdrivers/phantomjs')


def close():
    print("browser closed")
    browser.close()
