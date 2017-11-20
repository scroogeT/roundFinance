# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(members)
admin.site.register(memberState)
admin.site.register(transactionState)
admin.site.register(transactions)
