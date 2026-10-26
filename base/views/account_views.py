from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from base.models import Profile
from base.forms import UserCreationForm
from django.contrib import messages
 
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/login/'
    template_name = 'pages/login_signup.html'
 
    def form_valid(self, form):
        messages.success(self.request, '新規登録が完了しました。続けてログインしてください。')
        return super().form_valid(form)
 
 
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
 
    # 💡 get_object の中身を「return self.request.user」だけに書き換えます
    def get_object(self):
        return self.request.user

    # 💡 縦のライン（インデント）のズレを綺麗に修正しています
    def form_valid(self, form):
        messages.success(self.request, 'アカウント情報を更新しました。')
        return super().form_valid(form)
 
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'pages/profile.html'
    fields = ('name', 'zipcode', 'prefecture',
              'city', 'address1', 'address2', 'tel')
    success_url = '/profile/'
 
    # 💡 エラーを回避するため、user.profile を直接返すように書き換えます
    def get_object(self):
        return self.request.user.profile

    # 💡 プロフィール保存時にもメッセージ（通知）が出るように追加しています
    def form_valid(self, form):
        messages.success(self.request, 'プロフィール情報を更新しました。')
        return super().form_valid(form)
    