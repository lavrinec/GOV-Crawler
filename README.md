# GOV-Crawler

## Requirements

### OS

Short version: Pick any Linux distro you like.

Long version: We don't have enough time to play with pip-env.
So it's best that this project is executed on Linux 
as it can be tricky to get Python libraries to work on Windows 
and MacOS is available just on overpriced underpowered machines 
where you hit thermal throttling when running more demanding tasks 
because Apple thinks silence is more important than cooling.


### Python

Download Python 3.6 or 3.7 from [website](https://www.python.org/downloads/). 
We don't guarantee that all libraries work with lower 3.x sub-versions. 
Do not use Python 2.7.

#### Libraries

- Selenium: install Selenium by running `pip install selenium` in console
  - Linux: if you get an `EnvironmentError`, run `pip install selenium --user`


### Browser
The project uses Selenium which utilizes Chrome for headless browser.
The ChromeDriver is already provided in the project, so make sure you install Chrome.

- Chrome: Go to [Chrome website](https://www.google.com/chrome/) and download and install it.
  - or don't if you already have it and you are brave enough, just make sure it's version 71, 72 or 73
  - Linux: Do not use `snap` or other tools for installing Chrome.
