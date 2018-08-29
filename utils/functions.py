
import random
from datetime import datetime

from users.models import UserTicket


def get_random_ticket():
    # 获取随机字符串
    s='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    ticket = ''
    for i in range(30):
        ticket += random.choice(s)
    return ticket


def is_login(request):
    ticket = request.COOKIES.get('ticket')
    if ticket:
        user_ticket = UserTicket.objects.filter(ticket=ticket).first()
        if datetime.utcnow() < user_ticket.out_time.replace(tzinfo=None):
            user = user_ticket.user
            return user
    return None
