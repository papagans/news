from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from .forms import UserCreationForm, UserPasswordChangeForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin


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