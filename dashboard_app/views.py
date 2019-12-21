from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from dashboard_app.models import Query, Answer, Appointment
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models.functions import TruncDate
from django.db.models import Count
from datetime import datetime, timedelta

class Dashboard(View):

    @method_decorator(login_required(login_url='/'))
    def get(self, request):
        query = Query.objects.filter(replied=False).filter(closed=False).order_by('-asked_On')
        context_send = {'queries': query, 'pending': getAppointment()}
        return render(request, 'dashboard.html', context=context_send)

    def post(self, request):
        pass


class QueryViewThread(View):

    @method_decorator(login_required(login_url='/'))
    def get(self, request, value):
        if value:
            query = Query.objects.get(pk=value)
            query_reply = Answer.objects.filter(replied_to=value).order_by('replied_on')
            context_send = {'queries': query, 'replies': query_reply, 'pending': getAppointment()}
            return render(request, 'answer_query.html', context=context_send)
        else:
            query = Query.objects.order_by('-asked_On', 'replied')
            context_send = {'queries': query, 'pending': getAppointment()}
            return render(request, 'query.html', context=context_send)

    @method_decorator(login_required(login_url='/'))
    def post(self, request, value):
        user = User.objects.get(pk=request.user.id)
        question = Query.objects.get(pk=value)
        answer = request.POST['answer']

        Answer(replied_by=user, replied_to=question, reply=answer).save()
        question.replied = True
        question.save()
        return HttpResponseRedirect(reverse('query', args=(value,)))


class PendingViewThread(View):
    @method_decorator(login_required(login_url='/'))
    def get(self, request, id):
        if id:
            appointment = Appointment.objects.get(pk=id)
            appointed = Appointment.objects.annotate(date=TruncDate('day_of_appointment')).values('date').annotate(
                c=Count('id'))
            print(appointed)
            print(appointed)
            print(appointed)
            print(appointed)
            context_send = {'appointment': appointment, 'appointed': appointed, 'pending': getAppointment()}
            return render(request, 'appoint.html', context=context_send)
        else:
            appointments = Appointment.objects.filter(appointed=False)
            context_send = {'appointments': appointments, 'pending': getAppointment()}
            return render(request, 'pending.html', context=context_send)

    @method_decorator(login_required(login_url='/'))
    def post(self, request, id):
        appointment = Appointment.objects.get(pk=id)
        latest=Appointment.objects.latest('day_of_appointment')
        appointment.appointed=True
        appointment.day_of_appointment=latest.day_of_appointment+timedelta(hours=1)
        appointment.save()
        return HttpResponseRedirect(reverse('appoint'))


def getAppointment():
    count = Appointment.objects.filter(appointed=False).count()
    if count >= 1:
        return True
    else:
        return False
