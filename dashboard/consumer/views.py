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
        return Message.objects.filter(
            timestamp__gte = datetime.date.today()
        ).order_by("-timestamp")

    #def post_queryset(self,request):
