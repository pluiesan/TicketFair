from django.views.generic import ListView, DetailView
from base.models import Order
from django.contrib.auth.mixins import LoginRequiredMixin
import qrcode
import io
import base64


from base.models.order_models import MyTicket
 
 
class OrderIndexView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'pages/orders.html'
    ordering = '-created_at'
 
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
 
 
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'pages/order.html'
    
    # ＊get_querysetメソッドの追記
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
 

class MyTicketView(LoginRequiredMixin, ListView):
    model = MyTicket
    template_name = 'pages/my_ticket.html'

    def get_queryset(self):
        return MyTicket.objects.filter(user=self.request.user).order_by('-created_at')
 

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = MyTicket
    template_name = 'pages/ticket_detail.html'

    def get_queryset(self):
        return MyTicket.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        img = qrcode.make(context['myticket'].id)
        buffer = io.BytesIO() 
        img.save(buffer, format="PNG") 
        base64Img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
        context['taskGraphBase64'] = base64Img


        return context