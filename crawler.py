import time

import requests
from pyquery import PyQuery as pq
import settings
import os
from urllib import parse


VISITED_URLS = []

def update_visited_url(url: str):
    VISITED_URLS.append(url)
    with open(settings.VISITED_URL_FILES, 'a') as f:
        f.write('{}\n'.format(url))

def download_document(document_url: str):
    print('find document to download: {}'.format(document_url))
    url_path_parse_result  = parse.urlsplit(document_url)

    file_path = os.path.join(settings.PROJECT_BASE_DIR, *url_path_parse_result.path.split('/'))
    if os.path.exists(file_path):
        print('file already downloaded, skip this document.')
        return

    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    print('downloading...')
    start = time.time()
    response = requests.get(document_url)
    with open(file_path, 'wb') as fd:
        fd.write(response.content)

    end = time.time()
    print('download file into: {}, takes {} s'.format(file_path, end - start))
    update_visited_url(document_url)

def crawl_url(start_url):
    if start_url in VISITED_URLS:
        print('the url has been visited')
        return

    response = requests.get(start_url)
    document_pq = pq(response.text)
    a_href_list = document_pq('a')
    for idx in range(len(a_href_list)):
        if idx == 0:
            continue
        sub_dir_url = pq(a_href_list[idx]).attr('href')

        if sub_dir_url.endswith('.PDF'):
            document_url = '{}{}'.format(settings.HOST, sub_dir_url)
            if document_url in VISITED_URLS:
                print('find document: {} already visited. skip'.format(document_url))
                continue
            download_document(document_url)

        else:
            print('find url {}, need to go deeper'.format(sub_dir_url))
            crawl_url('{}{}'.format(settings.HOST, sub_dir_url))

    print('complete url: {}'.format(start_url))
    update_visited_url(start_url)
    return


def load_visited_urls():
    if not os.path.exists(settings.VISITED_URL_FILES):
        return

    with open(settings.VISITED_URL_FILES, 'r') as f:
        for line in f.readlines():
            VISITED_URLS.append(line.strip())


def main():
    load_visited_urls()
    crawl_url(settings.START_PAGE_URL)


if __name__ == '__main__':
    main()