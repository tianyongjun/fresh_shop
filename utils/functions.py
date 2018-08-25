
import random


def get_random_ticket():
    # 获取随机字符串
    s='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    ticket = ''
    for i in range(30):
        ticket += random.choice(s)
    return ticket
