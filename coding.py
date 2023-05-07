import math
from enum import Enum


class EncodeType(Enum):
    BINARY = 'BINARY'
    GRAY_CODE = 'GRAY_CODE'


def flip_num(num):
    return 0 if num != 0 else 1


def float_bin(number, places=3):
    whole, dec = str(number).split(".")
    whole = int(whole)
    dec = int(dec)
    res = bin(whole).lstrip("0b") + "."

    for x in range(places):
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole

    return res


def decimal_converter(num):
    while num > 1:
        num /= 10
    return num


def to_decimal(gray_code_arr):
    bin_arr = gray_to_binary(gray_code_arr)
    str_bin_code = "".join([str(x) for x in bin_arr])
    return int(str_bin_code, 2)


def split_str_code(s):
    return [int(ch) for ch in s]


def gray_to_binary(gray):
    n = int("".join([str(x) for x in gray]), 2)
    mask = n
    while mask != 0:
        mask >>= 1
        n ^= mask
    return split_str_code(bin(n)[2:])


def binary_to_gray(bin_arr):
    n = "".join([str(x) for x in bin_arr])
    n = int(n, 2)
    n ^= n >> 1
    return bin(n)[2:]


def encode_bin(x, a, b, m):
    n = int((x - a) * (2 ** m - 1) / (b - a))
    code = bin(n)[2:]
    while len(code) < m:
        code = "0" + code
    return split_str_code(code)


def decode_bin(code, a, b, m):
    str_code = "".join([str(x) for x in code])
    return round(a + int(str_code, 2) * ((b - a) / (math.pow(2, m) - 1)), 2)


def encode(x, a, b, m):
    code_bin = encode_bin(x, a, b, m)
    gray_code = binary_to_gray(code_bin)
    while len(gray_code) < m:
        gray_code = "0" + gray_code
    return split_str_code(gray_code)


def decode(code, a, b, m):
    code_bin = gray_to_binary(code)
    return decode_bin(code_bin, a, b, m)
