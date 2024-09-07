import glob
import json
import os
import random
from cProfile import label

from androguard.decompiler.dad.ast import local

from modules.cli.user_config import UserConfig
from modules.enums import DownloadType


class Parser:
    RANGE_ARGS_DELIMITER = ':'
    LIST_ARGS_DELIMITER = ','
    METADATA_DEFAULT_VALUE = ['sha256', 'pkg_name', 'apk_size', 'dex_date', 'markets']

    def __init__(self, args):
        self.args = args

    def parse(self, exist_sha256):
        number = int(self.args.number) if self.args.number else DownloadType.ALL
        dex_date_from, dex_date_to = self.args.dexdate.split(self.RANGE_ARGS_DELIMITER) if self.args.dexdate else (None, None)
        apksize_from, apksize_to = self.args.apksize.split(self.RANGE_ARGS_DELIMITER) if self.args.apksize else (None, None)
        vt_detection_from, vt_detection_to = self.args.vtdetection.split(self.RANGE_ARGS_DELIMITER) if self.args.vtdetection else (None, None)
        markets = self.args.markets.split(self.LIST_ARGS_DELIMITER) if self.args.markets else None
        pkg_name = self.args.pkgname.split(self.LIST_ARGS_DELIMITER) if self.args.pkgname else None
        sha256 = None
        label_map = None
        print(f'[+] sha256: {self.args.sha256}, type: {type(self.args.sha256)}')
        if os.path.isfile(self.args.sha256):
            # read sha256 from file
            print(f'[+] sha256 is file')
            with open(self.args.sha256) as file:
                sha256 = [line.strip().upper() for line in file]
        elif os.path.isdir(self.args.sha256):
            # read sha256 from dir
            print(f'[+] sha256 is dir')
            files = glob.glob(self.args.sha256 + os.sep + '*_malware.txt')
            sha256 = []
            label_map = dict()
            for file in files:
                year = os.path.basename(file).split('_')[0]
                label = os.path.basename(file).split('_')[1]
                all_sha256 = []
                with open(file, 'r') as f:
                    for line in f:
                        all_sha256.append(line.strip().upper())
                random.shuffle(all_sha256)
                tmp_sha256 = all_sha256[:2000] if label == 'trojan' or label == 'adware' else all_sha256
                for line in tmp_sha256:
                    label_map[line] = (year, label)
                    sha256.append(line)
        elif self.args.sha256 and not sha256:
            print(f'[+] sha256 is str')
            # split sha256, format:xxx,xxx,xxx
            sha256 = self.get_hash_list(self.args.sha256)
        #sha256 = self.get_hash_list(self.args.sha256) if self.args.sha256 else None
        sha1 = self.get_hash_list(self.args.sha1) if self.args.sha1 else None
        md5 = self.get_hash_list(self.args.md5) if self.args.md5 else None
        metadata = self.args.metadata.split(self.LIST_ARGS_DELIMITER) if self.args.metadata else self.METADATA_DEFAULT_VALUE
        key, input_file = self.args.key, self.args.input_file
        if not key or not input_file:
            user_config = UserConfig(key, input_file)
            input_file = input_file if input_file else user_config.in_file
            key = key if key else user_config.key

        if sha256:
            new_sha256 = list(set(sha256) - exist_sha256)
            sha256 = new_sha256
            print(f'[+] sha256 len: {len(sha256)}, type: {type(sha256)}')
        return number, dex_date_from, dex_date_to, apksize_from, apksize_to, vt_detection_from, vt_detection_to, markets, pkg_name, sha256, sha1, md5, metadata, key, input_file, label_map

    def get_hash_list(self, apk_hashes):
        return [apk_hash.upper() for apk_hash in apk_hashes.split(self.LIST_ARGS_DELIMITER)]

    def get_mapping(self, label_dir):
        if not os.path.exists(label_dir):
            print(f'proposed dir not exist')
            raise FileNotFoundError(f'label_dir: {label_dir}')
        files = glob.glob(label_dir + os.sep + '*' + os.sep + 'proposed.json')
        res = dict()
        for file in files:
            with open(file, 'r') as f:
                data = json.load(f)
                res.update(data)
        new_res = {k.upper(): v for k, v in res.items()}
        return new_res