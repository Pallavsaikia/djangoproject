from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from dashboard_app.models import Query, Answer
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


class Dashboard(View):

    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        query = Query.objects.filter(replied=False)
        context_send = {'queries': query}
        return render(request, 'dashboard.html', context=context_send)

    def post(self, request):
        pass


class QueryView(View):

    @method_decorator(login_required(login_url='/'))
    def get(self, request, value):
        query = Query.objects.get(pk=value)
        query_reply = Answer.objects.filter(replied_to=value).order_by('replied_on')
        context_send = {'queries': query, 'replies': query_reply}
        return render(request, 'answer_query.html', context=context_send)

    @method_decorator(login_required(login_url='/'))
    def post(self, request, value):
        user = User.objects.get(pk=request.user.id)
        question = Query.objects.get(pk=value)
        answer = request.POST['answer']

        Answer(replied_by=user, replied_to=question, reply=answer).save()
        question.replied = True
        question.save()
        return HttpResponseRedirect(reverse('query', args=(value,)))
