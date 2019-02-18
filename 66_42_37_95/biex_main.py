import monitor, variable, const, util

variable.BIEX_API_KEY = 'EO1bUXWlX8cPYWs4CKrUOMDf2oQ2H2f0ncdMnxCmLrJpXmb_Fogo9eaECeHBl_tG'
variable.BIEX_SECRET = 'IKC8jSDq9nrPKz4_WEqBXWWsxlOEzV6izpIIenaL4_Z23XJL'

# variable.BIEX_API_KEY = 'QH1FenUtmdEhEW1gpje3uFFD1EfJ09fmeSiFLMIgnMXhzUELTAbM5NPFaqecyVrA'
# variable.BIEX_SECRET = 'F4jTNXqsJbLle3zkQilXG9OYA2UcRZpKDW06W0V3ueP0NeyJ'

variable.TARGET_SITE = const.BIEX  # which site, for example BBX
variable.TARGET_SITE_URL = util.get_target_site_url(const.BIEX, const.ETH_REVERSE)  # site detail url, combine ticker
variable.TARGET_STRATEGY = const.STRATEGY_TEMP_BIEX  # which strategy

variable.CURRENT_ID = const.ETH_REVERSE  # which coin for ETH
variable.THRESHOLD = 0.5  # diff between bm and target
variable.CLOSE_THRESHOLD = 0.2  # close when diff between bm and target below
variable.MAX_AMOUNT = 3000  # max amount per open

# old strategy required
variable.CLOSE_DIFF = 0.1
monitor.ready()
