from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import redirect
from base.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from base.models import User
from django.utils.crypto import get_random_string

 
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("index")
    template_name = 'pages/login_signup.html'
 
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response

def guest_login(request):
    user = User()
    # user.username = get_random_string(10)
    user.username = f'{get_random_string(10)}(ゲスト)'
    user.email = get_random_string(10) + '@email.com'
    user.save()
    guest_user = User.objects.get(email=user.email)
    login(request, guest_user, backend='django.contrib.auth.backends.ModelBackend')
    messages.success(request, 'ゲストユーザーでログインしました。')
    return redirect('index')
 
class Login(LoginView):
    template_name = 'pages/login_signup.html'
 
    def form_valid(self, form):
        messages.success(self.request, 'ログインしました。')
        return super().form_valid(form)
 
    def form_invalid(self, form):
        messages.error(self.request, 'エラーでログインできません。')
        return super().form_invalid(form)
 
 
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'pages/account.html'
    fields = ('username', 'email',)
    success_url = '/account/'

    def get_object(self):
        # URL変数ではなく、現在のユーザーから直接pkを取得
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()




 

