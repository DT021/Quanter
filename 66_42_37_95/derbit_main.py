import monitor, variable, const, util

variable.BM_KEY = 'w6EBthx23_7otgxSYkCTSL2q'
variable.BM_SECRET = 'ZHBOJ9Qbzn52gRCEP4i2osyiNJlKc6jRAj__xspOL2rwz3qq'

variable.DB_API_KEY = '5SFJJZNaZVbeE'
variable.DB_SECRET = 'PZ45FI47HLEVJGNIH5M5IKNTUHKF5ZFF'

variable.TARGET_SITE = const.DERIBIT  # which site, for example BBX
variable.TARGET_SITE_URL = util.get_target_site_url(const.DERIBIT, const.BTC_REVERSE)  # site detail url, combine ticker
variable.TARGET_STRATEGY = const.STRATEGY_HEDGE  # which strategy

variable.CURRENT_ID = const.BTC_REVERSE  # which coin for ETH
variable.THRESHOLD = 8  # diff between bm and target
variable.CLOSE_THRESHOLD = 0.2  # close when diff between bm and target below
variable.MAX_AMOUNT = 1000  # max amount per open

monitor.ready()
