# ZEIT E-Paper to Thalia/Tolino cloud synchronization

Easy way of uploading the latest [ZEIT E-Paper](https://www.zeit.de/) to the [Thalia/Tolino cloud](https://mytolino.de/die-tolino-cloud/).

By using Selenium, the latest ZEIT ePub is downloaded and directly uploaded to the Tolino library.

By synchronizing the library on your Tolino e-Reader, one can read the news there.

**Requires a paid subscription for ZEIT Digital.**

## Configuration

### Installing dependencies

Google Chrome is used as a selenium webdriver. [Find out how to install the webdriver here.](https://chromedriver.chromium.org/home)

Furthermore, install the required Python 3 dependencies:

``` 
$ pip3 install urllib3 selenium
``` 

### Creating a configuration file

Create a configuration file named `config.yml` looking like this:

``` 
zeit:
  username: your_username
  password: your_password

thalia:
  username: your_username
  password: your_password
``` 

containing your respective credentials for ZEIT and Thalia.

## Running it

``` 
$ python3 main.py
``` 

### Creating a cron-job

Run it as a cron-job on a Raspberry PI every Wednesday at 6pm, just after the latest issue is released:

``` 
0 18 * * 3 /usr/bin/python3 /path/to/main.py 2>&1
``` 
 