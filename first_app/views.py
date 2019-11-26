from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth import login,logout
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        return render(request, 'index.html')

    def post(self, request):
        user = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=user, password=password, is_superuser=True)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("/dashboard/")

        else:
            logout(request)
            return redirect('/')

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect("/")
