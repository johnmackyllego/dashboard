# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'raw', 'timestamp')

admin.site.register(Message, MessageAdmin)
