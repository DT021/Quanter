import monitor, variable, const, util

variable.BBX_USERNAME = 'q211262712@163.com'
variable.BBX_PASSWORD = '920802ymy'

variable.TARGET_SITE = const.BBX  # which site, for example BBX
variable.TARGET_SITE_URL = util.get_target_site_url(const.BBX, const.BTC)  # site detail url, combine ticker
variable.TARGET_STRATEGY = const.STRATEGY_OLD  # which strategy

variable.CURRENT_ID = const.BTC  # which coin for ETH
variable.THRESHOLD = 8  # diff between bm and target
variable.CLOSE_THRESHOLD = 3  # close when diff between bm and target below
variable.MAX_AMOUNT = 5000  # max amount per open

# old strategy required
variable.CLOSE_DIFF = 3

monitor.ready()
