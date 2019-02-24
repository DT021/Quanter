from api.bbx_api import BbxApi
from api.bitmex_api import BitmexApi
from api.db_api import DeribitApi
from api.biex_api import BiexApi
from api.bybit_api import BybitApi
import variable, const

site_api = None
bitmex_api = None


def get_bitmex_api():
    global bitmex_api
    if bitmex_api is None:
        bitmex_api = BitmexApi()
    return bitmex_api


def get_site_api():
    global site_api
    if site_api is not None:
        return site_api

    if variable.TARGET_SITE == const.BBX:
        site_api = BbxApi()
    elif variable.TARGET_SITE == const.DERIBIT:
        site_api = DeribitApi()
    elif variable.TARGET_SITE == const.BIEX:
        site_api = BiexApi()
    elif variable.TARGET_SITE == const.BYBIT:
        site_api = BybitApi()

    if site_api is None:
        print('api init failed')
        return

    return site_api
