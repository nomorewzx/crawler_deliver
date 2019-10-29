import os

START_PAGE_URL = 'https://www.etsi.org/deliver/'
HOST = 'https://www.etsi.org'
VISITED_URL_FILES = 'visited_url.txt'
CANNOT_DOWNLOAD_FILES = 'cannot_download.txt'
PROJECT_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_MAX_TRY = 3