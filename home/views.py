from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import View

@method_decorator(login_required, name = 'dispatch')
class Home(View):
    def render(self, request):
        return render(request, './home/home.html')

    def get(self, request):
        return self.render(request)

@method_decorator(login_required, name = 'dispatch')
class Name(View):
    def render(self, request):
        return render(request, './home/name.html')

    def get(self, request):
        return self.render(request)

@method_decorator(login_required, name = 'dispatch')
class Surf(View):
    def render(self, request):
        return render(request, './home/surf.html')

    def get(self, request):
        return self.render(request)

# class Signup(View):
#     def render(self, request, form = None):
#         form = form if form else RegisterForm()
#         return render(request, './accounts/register/register.html', {'form': form})
#     def post(self, request):
#         form = RegisterForm(request.POST)

#         if form.is_valid():
#             form.save()
#             return redirect('login')

#         return self.render(request, form)

#     def get(self, request):
#         return self.render(request)