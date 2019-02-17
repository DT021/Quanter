import hashlib
import time
import requests
import json
import variable


def md5(target):
    m3 = hashlib.md5()
    m3.update(target.encode())
    result_str = m3.digest()
    real_result = ''
    for b in result_str:
        real_result += '%02x' % int(b & 0xFF)
    return real_result


def get_login_header(time_stamp):
    headers = {
                'Bbx-Dev': 'web',
                'Bbx-Language': 'zh-cn',
                'Bbx-Ts': str(time_stamp) + '000',
                'Bbx-Ver': '1.0',
                'Origin': 'https://www.bbx.com',
                'Referer': 'https://www.bbx.com/login?lang=zh-CN&qd=null'
    }
    return headers


def get_login_data():
    time_stamp = int(time.time() * 1000)
    nonce = str(time_stamp) + '000'
    data = {
                'account_type': 1,
                'email': variable.BBX_USERNAME,
                'nonce': int(nonce),
                'password': md5(md5(variable.BBX_PASSWORD)+nonce)
    }
    return data


def get_token_uid():
    time_stamp = int(time.time() * 1000)
    response = requests.post('https://api.bbxapp.vip/v1/ifaccount/login?t=' + str(time_stamp),
                             headers=get_login_header(time_stamp), data=json.dumps(get_login_data()))
    response_header = response.headers
    print(response.text)
    print(response_header)
    token = response_header['Bbx-Token']
    uid = response_header['Bbx-Uid']
    variable.BBX_TOKEN = token
    variable.BBX_UID = uid
    return token, uid
