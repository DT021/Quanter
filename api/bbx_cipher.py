#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
key = '5ffF03b858D5Fd16'
char = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']


def encrypt(token, time_stamp):
    result = ''
    generator = AES.new(key, AES.MODE_CBC, time_stamp)
    crypt = generator.encrypt(pad(token))
    for b in crypt:
        m = 0xF & b >> 4
        n = 0xF & b
        result += char[m]
        result += char[n]
    return result[0:64]


# encrypt('19e3064f2a27d496af5ce610e8e3a7d0', '1548082072579000')