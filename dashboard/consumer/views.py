# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from models import Message
from django.views.generic.base import TemplateView
from django.views import generic
import datetime

# Create your views here.
class MessageView(generic.ListView):
    template_name='home.html'
    context_object_name = 'message_list'
    query_results = Message.objects.all()
    
    def get_queryset(self):
        start_date = self.request.GET.get("datetimepicker1")
        end_date = self.request.GET.get("datetimepicker2")
        
        if start_date and end_date:
            s_date = datetime.datetime.strptime(start_date,'%Y/%m/%d %H:%M')
            e_date = datetime.datetime.strptime(end_date,'%Y/%m/%d %H:%M')

            if s_date <= e_date:
                return Message.objects.filter(
                    timestamp__range = (s_date, e_date)
                ).order_by("-timestamp")
            else:
                return Message.objects.filter(
                    timestamp__range = (e_date, s_date)
                ).order_by("-timestamp")
        else:
            return Message.objects.filter(
                timestamp__gte = datetime.date.today()
            ).order_by("-timestamp")