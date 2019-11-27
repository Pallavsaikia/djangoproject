from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from dashboard_app.models import Query


class Dashboard(View):

    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        query = Query.objects.filter(replied=False)
        context_send = {'queries': query}
        return render(request, 'dashboard.html', context=context_send)

    def post(self, request):
        pass
