import json
import os
import os.path
import requests

from enum import Enum
from pathlib import Path

class CacheOption(Enum):
    DEFAULT = 1
    SKIP_MEM_CACHE = 2
    SKIP_DISK_CACHE = 3
    CLEAR_DISK_CACHE = 4

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return CacheOption[s]
        except KeyError:
            raise ValueError()

class CA_DMV():
    API_ROOT = "https://www.dmv.ca.gov/wasapp/ipp2"
    PATH_INIT = "initPers.do"
    PATH_START = "startPers.do"
    PATH_PROCESS = "processPers.do"
    PATH_PLATE = "processConfigPlate.do"

    START_DATA = {
        "acknowledged": "true",
        "_acknowledged": "on",
    }
    PROCESS_DATA = {
        "imageSelected": "none",
        "vehicleType": "AUTO",
        "licPlateReplaced": "GITHUB",
        "last3Vin": "166",
        "isRegExpire60": "no",
        "isVehLeased": "no",
        "plateType": "R",
    }
    PLATE_DATA = {
            "kidsPlate": "",
            "plateType": "R",
            "plateLength": "7",
            "plateNameLow": "environmental",
            "plateChar0": "",
            "plateChar1": "",
            "plateChar2": "",
            "plateChar3": "",
            "plateChar4": "",
            "plateChar5": "",
            "plateChar6": "",
        }
    PLATE_CHAR_PREFIX = "plateChar"
    MIN_LENGTH = 2
    MAX_LENGTH = 7
    SUCCESS_PHRASE = "id=\"PersonalizedFormBean\""
    FAILURE_PHRASE = "id=\"plate-configurator\""

    CACHE_PATH = "~/.cache/vanity/ca_dmv.json"

    def __init__(self, cache_option = CacheOption.DEFAULT):
        self.session = None
        self.cache = None
        self.cache_option = cache_option
        if self.cache_option == CacheOption.CLEAR_DISK_CACHE:
            self.clear_cache()

    def initialize(self):
        self.check_cache_initialized(force = True)
        self.check_session_initialized(force = True)

    def check_plate(self, word):
        cached = self.cache_read(word)
        if cached is not None:
            return cached
        self.check_session_initialized()
        data = CA_DMV.build_plate_request_data(word)
        if not data:
            print("Invalid input, can't check the DMV.")
            return False
        result = self.session.post(
            url = CA_DMV.dmv_url(CA_DMV.PATH_PLATE),
            data = data,
        )
        available = CA_DMV.check_plate_response(result)
        if available is None:
            print("Got an unknown result for a plate, neither success nor failure!")
            return False
        self.cache_write(word, available)
        self.commit_cache()
        return available

    def check_session_initialized(self, force = False):
        if self.session is None or force:
            self.session = CA_DMV.init_dmv_session()

    def check_cache_initialized(self, force = False):
        if self.cache_option == CacheOption.SKIP_MEM_CACHE:
            return False
        if self.cache is None or force:
            if self.cache_option == CacheOption.SKIP_DISK_CACHE:
                self.cache = {}
            else:
                try:
                    with open(CA_DMV.get_cache_path()) as cache_file:
                        self.cache = json.load(cache_file)
                except (FileNotFoundError, PermissionError, json.JSONDecodeError) as ex:
                    self.cache = {}
        return True

    def cache_read(self, word):
        if self.check_cache_initialized():
            return self.cache.get(word)
        else:
            return None

    def cache_write(self, word, value):
        if self.check_cache_initialized():
            self.cache[word] = value

    def commit_cache(self):
        if self.check_cache_initialized() and self.cache_option != CacheOption.SKIP_DISK_CACHE:
            cache_dir = Path(CA_DMV.get_cache_path()).parent
            cache_dir.mkdir(parents=True, exist_ok=True)
            with open(CA_DMV.get_cache_path(), "w") as cache_file:
                json.dump(self.cache, cache_file)

    def clear_cache(self):
        try:
            os.remove(CA_DMV.get_cache_path())
        except FileNotFoundError:
            pass

    def get_cache_path():
        return os.path.expanduser(CA_DMV.CACHE_PATH)

    def dmv_url(page):
        return "{}/{}".format(CA_DMV.API_ROOT, page)

    def init_dmv_session():
        session = requests.Session()
        session.get(url = CA_DMV.dmv_url(CA_DMV.PATH_INIT))
        session.post(
            url = CA_DMV.dmv_url(CA_DMV.PATH_START),
            data = CA_DMV.PROCESS_DATA,
        )
        session.post(
            url = CA_DMV.dmv_url(CA_DMV.PATH_PROCESS),
            data = CA_DMV.START_DATA,
        )
        return session

    def build_plate_request_data(word):
        if len(word) < CA_DMV.MIN_LENGTH or len(word) > CA_DMV.MAX_LENGTH:
            return None
        data = CA_DMV.PLATE_DATA.copy()
        for idx, char in enumerate(word):
            param = "{}{}".format(CA_DMV.PLATE_CHAR_PREFIX, idx)
            data[param] = char
        return data

    def check_plate_response(response):
        if CA_DMV.SUCCESS_PHRASE in response.text:
            return True
        elif CA_DMV.FAILURE_PHRASE in response.text:
            return False
        else:
            return None
