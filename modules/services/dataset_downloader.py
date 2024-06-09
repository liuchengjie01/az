import logging
import multiprocessing
import os
import sys

import requests
import time

from modules.services.url_constructor import UrlConstructor


class DatasetDownloader:
    def __init__(self, dataset, threads, url_constructor=None, key='', out_dir='azoo_dataset'):
        self.dataset = dataset
        self.out_dir = out_dir
        if not url_constructor:
            url_constructor = UrlConstructor(key)
        self.url_constructor = url_constructor
        self.threads = threads

    def download(self, num):
        logging.info(f'DOWNLOADING {len(self.dataset)}, number of threads {self.threads}')
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        with multiprocessing.Manager() as manager:
            download_cnt = manager.Value('i', num)
            stop_event = manager.Event()
            lock = manager.Lock()
            map_args = [(apk, download_cnt, stop_event, lock) for apk in self.dataset]
            with multiprocessing.Pool(self.threads) as pool:
                results = []
                for result in pool.starmap(self.download_apk,map_args):
                    if stop_event.is_set():
                        pool.terminate()
                        break

    def download_apk(self, apk, cnt, stop_event, lock):
        with lock:     
            if stop_event.is_set():
                return
        apk_save_path = os.path.join(self.out_dir, apk.sha256) + '.apk'
        try:
            if os.path.exists(apk_save_path):
                return
                apk_save_path = apk_save_path.replace('.apk', f'{apk.sha1}.apk')
                logging.warning(f'apk with pkg {apk.sha256} already exists, saving by {apk_save_path}')
            logging.debug(f'DOWNLOAD {apk.sha256}... ')
            apk_url = self.url_constructor.construct(apk)
            response = requests.get(apk_url)
            code = response.status_code
            if code != 200:
                logging.info(f'HTTP code for {apk.sha256} is {code}')
                time.sleep(1.5)
                resp = requests.get(apk_url)
                if resp.status_code == 200:
                    with lock:
                        cnt.value -= 1
                        if cnt.value <= 0:
                            stop_event.set()
                    with open(apk_save_path, 'wb') as out_file:
                        out_file.write(resp.content)
            else:
                with lock:
                    cnt.value -= 1
                    if cnt.value <= 0:
                        stop_event.set()
                with open(apk_save_path, 'wb') as out_file:
                    out_file.write(response.content)
        except:
            logging.error(f'Unexpected error while downloading {apk.sha256}: {sys.exc_info()[1]}')
