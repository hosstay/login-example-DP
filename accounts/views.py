from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.views.generic import View, UpdateView

from .forms import RegisterForm

class Register(View):
    def render(self, request, form = None):
        form = form if form else RegisterForm()
        return render(request, './accounts/register/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

        return self.render(request, form)

    def get(self, request):
        return self.render(request)

@method_decorator(login_required, name = 'dispatch')
class EditUser(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = './accounts/my_account/edit_user.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user
