# GOV-Crawler

## Requirements

### OS

Pick any Linux distro you like.


### Python

Download Python 3.6 or 3.7 from [Python website](https://www.python.org/downloads/). 
We don't guarantee that all libraries work with lower 3.x sub-versions. 
Do not use Python 2.7.

All further instructions are written with assumption that Python 3 is your default Python 
(be sure to check the PATH or write `python3` and `pip3` instead of `python` and `pip` ).

#### Libraries

- Selenium: install Selenium by running `pip install selenium` in console
  - Linux: if you get an `EnvironmentError`, run `pip install selenium --user`
- psycopg2 vs psycopg2-binary: `pip install psycopg2 --user`

- sqlalchemy: run `pip install sqlalchemy`, in case of `EnvironmentError` run `pip install sqlalchemy --user`


### Browser
The project uses Selenium which utilizes Chrome for headless browser.
The ChromeDriver is already provided in the project, so make sure you have Chrome.

- Chrome: Go to [Chrome website](https://www.google.com/chrome/) and download and install it.
  - or don't if you already have it and you are brave enough, just make sure it's version 71, 72 or 73 (hint: update)
  - Linux: Do not use `snap` or other tools for installing Chrome.


## Running

go to project root and run `python crawler.py <num_of_workers>`