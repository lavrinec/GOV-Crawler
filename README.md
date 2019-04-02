# GOV-Crawler

## Requirements

### Python

Download Python 3.6 or 3.7 from [Python website](https://www.python.org/downloads/). 
We don't guarantee that all libraries work with lower 3.x sub-versions. 
Do not use Python 2.7.

#### Note
All instructions are tested on Linux, we don't guarantee that everything will work on Windows or MacOS.
All further instructions are written with assumption that Python 3 is your default Python 
(be sure to check the PATH or write `python3` and `pip3` instead of `python` and `pip` ).

In case of `EnvironmentError`, run `pip install <module> --user`.
Or you can use pipenv. 
You need to install it first (`pip install pipenv`) and then run `pipenv shell`. 
Note that you must then install needed libraries with `pipenv` not `pip`.

#### Libraries

- Selenium: install Selenium by running `pip install selenium` in console
  - Note: webdriver for headless browser for Selenium is already provided

- psycopg2 vs psycopg2-binary: run `pip install psycopg2`

- sqlalchemy: run `pip install sqlalchemy`

- BeautifulSoup4: run `pip install bs4`

- requests: run `pip install requests`


## Running

go to project root and run `python crawler.py <num_of_workers>`