from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from .forms import UserCreationForm, UserPasswordChangeForm, UserPasswordResetForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from main.settings import HOST_NAME
from django.core.mail import send_mail
from accounts.models import Token
from django.conf import settings
from django.template.loader import get_template

class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'

    def test_func(self):
        return self.get_object() == self.request.user


class UserListView(ListView):
    template_name = 'user_list.html'
    model = User
    context_object_name = "users"

def test_func(self):
        return self.get_object() == self.request.user

class UserUpdateView(UpdateView):
    model = User
    context_object_name = 'user_object'
    template_name = 'partial/edit.html'
    fields = ['username', 'email']

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={"pk": self.object.pk})


class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = User
    context_object_name = 'object'
    template_name = 'partial/delete.html'
    success_url = reverse_lazy('accounts:user_list')
    permission_denied_message = "Доступ запрещен"

    def test_func(self):
        user = self.request.user
        return user.is_staff


class UserPasswordChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'partial/edit.html'
    form_class = UserPasswordChangeForm
    context_object_name = 'user_object'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse('accounts:login')


def register_view(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'partial/add.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                is_active=True
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect("accounts:user_list")
        else:
            return render(request, 'partial/add.html', {'form': form})


def password_reset_email_view(request):
    if request.method == 'GET':
        return render(request, 'password_reset_email.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)
        if len(users) > 0:
            user = users[0]
            token = Token.objects.create(user=user)
            redirect_url = 'accounts:password_reset_form'
            url = HOST_NAME + reverse(redirect_url, kwargs={'token': token})
            # send_token(user,
            #            'Вы запросили восстановление пароля на сайте localhost:8000.',
            #            'Для ввода нового пароля перейдите по ссылке: {url}',
            #            redirect_url='accounts:password_reset_form')
            context = {
                'user': user.first_name,
                'url': url,
                'h1': 'Забыли пароль?',
                'text': 'Не волнуйтесь - такое случается!',
                'text_2': 'Просто нажмите на кнопку ниже и создайте новый пароль. Проще не бывает!',
                'btn_text': 'Восстановить пароль'
            }
            send_mail('Восстановление пароля News', 'Восстановление пароля News', settings.EMAIL_HOST_USER, [user.email],
                      html_message=get_template('password_reset_emailing.html').render(context),
                      fail_silently=False)
        return render(request, 'password_reset_confirm.html')


class PasswordResetFormView(UpdateView):
    model = User
    template_name = 'password_reset_form.html'
    form_class = UserPasswordResetForm
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        token = self.get_token()
        return token.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['token'] = self.kwargs.get('token')
        return context

    def form_valid(self, form):
        token = self.get_token()
        token.delete()
        return super().form_valid(form)

    def get_token(self):
        token_value = self.kwargs.get('token')
        return get_object_or_404(Token, token=token_value)

    def get_success_url(self):
        return reverse('accounts:login')