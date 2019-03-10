# # Downloader: download and render a page on given URL
#
# import os
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
#
# chrome_options = Options()
# chrome_options.add_argument("--headless")
#
# # location of chrome (like exe file on Windows), not chrome driver !!!
# # find the location of Chrome and change this only if it doesn't work when commented out
# # chrome_options.binary_location = ''
#
# # chromedriver-2-46 can deal with Chrome 71, 72, 73
# # chromedriver-73 can only deal with Chrome 73
# # executable_path goes from the root of the project forward, not from current directory !!!
# driver = webdriver.Chrome(executable_path='./webdrivers/chromedriver-2-46', chrome_options=chrome_options)
# driver.get("http://fri.uni-lj.si")
#
# for n in driver.find_elements_by_class_name('news-container-title'):
#     if len(n.text) > 0:
#         print(n.text)
#
# driver.close()
