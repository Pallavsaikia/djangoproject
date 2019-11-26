from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator


class Dashboard(View):

    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        return render(request, 'dashboard.html')

    def post(self, request):
        pass
