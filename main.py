import argparse
import os
from datetime import date

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from download import download_file
from thalia_library import ThaliaLogin
from zeit_epaper import ZeitEPaper

DEFAULT_CONFIG_FILE = 'config.yml'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/84.0.4147.125 ' \
             'Safari/537.36'

# parse arguments

parser = argparse.ArgumentParser(description='Fetches the current ZEIT ePub file and adds it to the Tolino cloud.')
parser.add_argument('-c', '--config', dest='config', help='Configuration file', type=str)
args = parser.parse_args()

config_file = None
if args.config is not None:
    config_file = args.config

# base directory

abspath = os.path.abspath(__file__)
base_dir = os.path.dirname(abspath)

# load config

if config_file is None:
    config_file = f'{base_dir}/{DEFAULT_CONFIG_FILE}'

if not os.path.exists(config_file):
    parser.error(f'The file {config_file} does not exist.')

with open(config_file, 'r') as stream:
    config = yaml.safe_load(stream)

if 'zeit' not in config or 'thalia' not in config \
        or 'username' not in config['zeit'] or 'password' not in config['zeit']\
        or 'username' not in config['thalia'] or 'password' not in config['thalia']:
    raise Exception('Cannot find credentials in config file.')

# configure webdriver

chrome_options = Options()
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument(f'user-agent={USER_AGENT}')
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(5)

# download epub

epub_url = ZeitEPaper(driver)\
    .login(config['zeit']['username'], config['zeit']['password'])\
    .current_issue()\
    .get_download_url()

epub_path = f'{base_dir}/zeit-{date.today()}.epub'
download_file(epub_url, epub_path, driver.get_cookies())

ThaliaLogin(driver)\
    .login(config['thalia']['username'], config['thalia']['password'])\
    .upload(epub_path)

driver.close()
