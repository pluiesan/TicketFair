from django.core.management.base import BaseCommand
from base.models import Ticket, MyTicket
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ここに思い思いのスクリプトを記述する"""
        # 更新するチケット種を取得
        now = make_aware(datetime.now())
        an_hour_ago = make_aware(datetime.now() - timedelta(hours=1))
        tickets = Ticket.objects.filter(show_result_at__range=(an_hour_ago, now))
        # tickets = Ticket.objects.filter(show_result_at__lt=now)

        # 整理番号を追加する必要のあるマイチケットを取得
        for ticket in tickets:
            mytickets = MyTicket.objects.filter(ticket=ticket)
            for i, myticket in enumerate(mytickets.order_by('id'), 1):
                myticket.reference_number = i
                myticket.save()


