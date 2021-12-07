import requests

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

    def __init__(self):
        self.session = None

    def initialize(self):
        self.check_initialized(force = True)

    def checkPlate(self, word):
        self.check_initialized(force = False)
        data = CA_DMV.buildPlateRequestData(word)
        if not data:
            print("Invalid input, can't check the DMV.")
            return False
        result = self.session.post(
            url = CA_DMV.dmvUrl(CA_DMV.PATH_PLATE), 
            data = data,
        )
        available = CA_DMV.checkPlateResult(result)
        if available is None:
            print("Got an unknown result for a plate, neither success nor failure!")
            return False
        return available

    def check_initialized(self, force = False):
        if not self.session or force:
            self.session = CA_DMV.initDmvSession()

    def dmvUrl(page):
        return "{}/{}".format(CA_DMV.API_ROOT, page)

    def initDmvSession():
        session = requests.Session()
        session.get(url = CA_DMV.dmvUrl(CA_DMV.PATH_INIT))
        session.post(
            url = CA_DMV.dmvUrl(CA_DMV.PATH_START), 
            data = CA_DMV.PROCESS_DATA,
        )
        session.post(
            url = CA_DMV.dmvUrl(CA_DMV.PATH_PROCESS), 
            data = CA_DMV.START_DATA,
        )
        return session

    def buildPlateRequestData(word):
        if len(word) < CA_DMV.MIN_LENGTH or len(word) > CA_DMV.MAX_LENGTH:
            return None
        data = CA_DMV.PLATE_DATA.copy()
        for idx, char in enumerate(word):
            param = "{}{}".format(CA_DMV.PLATE_CHAR_PREFIX, idx)
            data[param] = char
        return data

    def checkPlateResult(response):
        if CA_DMV.SUCCESS_PHRASE in response.text:
            return True
        elif CA_DMV.FAILURE_PHRASE in response.text:
            return False
        else:
            return None