from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView, UpdateView
from .forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'


class UserListView(ListView):
    template_name = 'user_list.html'
    model = User
    context_object_name = "users"


class UserUpdateView(UpdateView):
    model = User
    # template_name = 'user_update.html'
    context_object_name = 'user_object'
    template_name = 'partial/edit.html'
    fields = ['username', 'email']
    # success_url = reverse_lazy('accounts:user_list', kwargs={"pk": object.pk})

    # def test_func(self):
    #     return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={"pk": self.object.pk})


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

            # токен для активации, его сложнее угадать, чем pk user-а.
            # token = Token.objects.create(user=user)
            # activation_url = HOST_NAME + reverse('accounts:user_activate') + \
            #                  '?token={}'.format(token)
            #
            # # отправка письма на email пользователя
            # user.email_user('Регистрация на сайте localhost',
            #                 'Для активации перейдите по ссылке: {}'.format(activation_url))
            # print(activation_url)
            return redirect("accounts:user_list")
        else:
            return render(request, 'partial/add.html', {'form': form})