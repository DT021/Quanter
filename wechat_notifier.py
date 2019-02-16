import requests
import variable, util

local_ip = ''


def set_ip(_ip):
    global local_ip
    local_ip = _ip


def send_message(msg):
    print(msg)
    data = {
            'use': util.get_bm_ticker(variable.CURRENT_ID),
            'email': variable.TARGET_SITE,
            'ip': local_ip,
            'message': msg
    }
    requests.post('http://45.77.18.23:8888/message', data=data)
