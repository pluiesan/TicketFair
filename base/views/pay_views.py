from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.conf import settings
from stripe.api_resources import tax_rate
from base.models import Event, Order
import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
 
stripe.api_key = settings.STRIPE_API_SECRET_KEY

class PaySuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/success.html'
 
    def get(self, request, *args, **kwargs):
        # 最新のOrderオブジェクトを取得し、注文確定に変更
        order = Order.objects.filter(
            user=request.user).order_by('-created_at')[0]
        order.is_confirmed = True  # 注文確定
        order.save()
 
        return super().get(request, *args, **kwargs)
 
 
class PayCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/cancel.html'
 
    def get(self, request, *args, **kwargs):
        # 最新のOrderオブジェクトを取得
        order = Order.objects.filter(
            user=request.user).order_by('-created_at')[0]
 
        # 在庫数と販売数を元の状態に戻す
        event = Event.objects.get(pk=order.event_pk)
        event.sold_count -= order.quantity
        event.stock += order.quantity
        event.save()
 
        # is_confirmedがFalseであれば削除（仮オーダー削除）
        if not order.is_confirmed:
            order.delete()
 
        return super().get(request, *args, **kwargs)
 
 
tax_rate = stripe.TaxRate.create(
    display_name='消費税',
    description='消費税',
    country='JP',
    jurisdiction='JP',
    percentage=settings.TAX_RATE * 100,
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)
 
 
def create_line_item(unit_amount, name, quantity):
    return {
        'price_data': {
            'currency': 'JPY',
            'unit_amount': unit_amount,
            'product_data': {'name': name, }
        },
        'quantity': quantity,
        'tax_rates': [tax_rate.id]
    }
 
 
class PayWithStripe(LoginRequiredMixin, View):
 
    def post(self, request, *args, **kwargs):
        line_items = []
        event_pk = request.POST.get('event_pk')
        quantity = int(request.POST.get('quantity'))
        event = Event.objects.get(pk=event_pk)
        line_item = create_line_item(
                event.price, event.name, quantity)
        line_items.append(line_item)

        # 在庫をこの時点で引いておく、注文キャンセルの場合は在庫を戻す
        # 販売数も加算しておく
        event.stock -= quantity
        event.sold_count += quantity
        event.save()

        # 仮注文を作成（is_confirmed=Flase)
        Order.objects.create(
            user=request.user,
            uid=request.user.pk,
            event_pk=event_pk,
            event_name=event.name,
            price=event.price,
            quantity=quantity,
            amount=event.price * quantity,
            tax_included=event.price * quantity * (settings.TAX_RATE + 1)
        )
 
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{settings.MY_URL}/pay/success/',
            cancel_url=f'{settings.MY_URL}/pay/cancel/',
        )
        return redirect(checkout_session.url)

