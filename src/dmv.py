import json
import logging
import os
import os.path
import platform
import requests
import sys

from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)

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

    APPNAME = "vanity"
    CACHE_FILE = "ca_dmv.json"

    def __init__(self, cache_option = CacheOption.DEFAULT):
        self.session = None
        self.cache = None
        self.cache_option = cache_option
        if self.cache_option == CacheOption.SKIP_MEM_CACHE:
            logger.debug("Not initializing cache due to option %s", self.cache_option)
        if self.cache_option == CacheOption.CLEAR_DISK_CACHE:
            self.clear_cache()

    def initialize(self):
        self.check_cache_initialized(force = True)
        self.check_session_initialized(force = True)

    def check_plate(self, word):
        logger.debug("Checking word: '%s'", word)
        cached = self.cache_read(word)
        if cached is not None:
            logger.debug("Found result in cache: ('%s': %s)", word, cached)
            return cached
        self.check_session_initialized()
        data = CA_DMV.build_plate_request_data(word)
        if not data:
            logger.error("Invalid input, can't check the DMV.")
            return False
        result = self.session.post(
            url = CA_DMV.dmv_url(CA_DMV.PATH_PLATE),
            data = data,
        )
        available = CA_DMV.check_plate_response(result)
        if available is None:
            logger.error("Got an unknown result for a plate, neither success nor failure!")
            return False
        logger.debug("Got result from API: ('%s': %s)", word, available)
        self.cache_write(word, available)
        self.commit_cache()
        return available

    def check_session_initialized(self, force = False):
        if self.session is None or force:
            logger.debug("Initializing DMV request session")
            self.session = CA_DMV.init_dmv_session()

    def check_cache_initialized(self, force = False):
        if self.cache_option == CacheOption.SKIP_MEM_CACHE:
            return False
        if self.cache is None or force:
            if self.cache_option == CacheOption.SKIP_DISK_CACHE:
                logger.debug("Not loading cache due to option %s", self.cache_option)
                self.cache = {}
            else:
                logger.debug("Loading cache from %s", CA_DMV.get_cache_path())
                try:
                    with open(CA_DMV.get_cache_path()) as cache_file:
                        self.cache = json.load(cache_file)
                        logger.debug("Successfully loaded %d entries from the cache", len(self.cache))
                except (FileNotFoundError, PermissionError, json.JSONDecodeError) as ex:
                    logger.debug("Failed to read cache from disk due to: %s", ex)
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
            logger.debug("Saving %d cache entries to %s", len(self.cache), CA_DMV.get_cache_path())
            cache_dir = Path(CA_DMV.get_cache_path()).parent
            cache_dir.mkdir(parents=True, exist_ok=True)
            with open(CA_DMV.get_cache_path(), "w") as cache_file:
                json.dump(self.cache, cache_file)

    def clear_cache(self):
        logger.debug("Clearing cache from %s", CA_DMV.get_cache_path())
        try:
            os.remove(CA_DMV.get_cache_path())
            logger.debug("Successfully cleared cache")
        except FileNotFoundError:
            logger.debug("Could not clear disk cache - does not exist")

    def get_cache_path():
        cache_dir = CA_DMV.user_cache_dir(CA_DMV.APPNAME)
        return os.path.join(cache_dir, CA_DMV.CACHE_FILE)

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

    # adapted from https://github.com/ActiveState/appdirs
    def user_cache_dir(appname):
        r"""Return full path to the user-specific cache dir for this application.

        "appname" is the name of application.

        Typical user cache directories are:
            Mac OS X:   ~/Library/Caches/<AppName>
            Unix:       ~/.cache/<AppName> (XDG default)
            Win XP:     C:\Documents and Settings\<username>\Local Settings\Application Data\<AppAuthor>\<AppName>\Cache
            Vista:      C:\Users\<username>\AppData\Local\<AppAuthor>\<AppName>\Cache
        On Windows the only suggestion in the MSDN docs is that local settings go in
        the `CSIDL_LOCAL_APPDATA` directory. This is identical to the non-roaming
        app data dir (the default returned by `user_data_dir` above). Apps typically
        put cache data somewhere *under* the given dir here. Some examples:
            ...\Mozilla\Firefox\Profiles\<ProfileName>\Cache
            ...\Acme\SuperApp\Cache\1.0
        """
        system = CA_DMV.get_system()
        if system == "win32":
            path = os.path.normpath(_get_win_folder("CSIDL_LOCAL_APPDATA"))
            path = os.path.join(path, appname)
            path = os.path.join(path, "Cache")
        elif system == "darwin":
            path = os.path.expanduser("~/Library/Caches")
            path = os.path.join(path, appname)
        else: # linux
            path = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
            path = os.path.join(path, appname)
        return path

    # adapted from https://github.com/ActiveState/appdirs
    def get_system():
        if sys.platform.startswith("java"):
            os_name = platform.java_ver()[3][0]
            if os_name.startswith("Windows"): # "Windows XP", "Windows 7", etc.
                return "win32"
            elif os_name.startswith("Mac"): # "Mac OS X", etc.
                return "darwin"
            else: # "Linux", "SunOS", "FreeBSD", etc.
                # Setting this to "linux2" is not ideal, but only Windows or Mac
                # are actually checked for and the rest of the module expects
                # *sys.platform* style strings.
                return "linux2"
        else:
            return sys.platform
