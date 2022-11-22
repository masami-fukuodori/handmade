"""utilモジュール"""

import string
ZERO_TO_Z_LIST = [str(i) for i in range(9)] + [i for i in string.ascii_letters]


def zen_to_han(x: str) -> str:
    """アルファベット・数字を半角に変換

    Args:
        x (str): _description_

    Returns:
        str: _description_
    """
    x = (x.translate(str.maketrans({chr(0xFF01 + i):
         chr(0x21 + i) for i in range(94)})))
    return x


def han_to_zen(x: str) -> str:
    """アルファベット・数字を全角に変換

    Args:
        x (str): 文字列

    Returns:
        str: 文字列
    """
    x = (x.translate(str.maketrans({chr(0x0021 + i):
         chr(0xFF01 + i) for i in range(94)})))
    return x
