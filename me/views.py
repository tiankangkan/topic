# -*- coding:utf-8 -*-

import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt


def reply_to_me(request):
    return render(request, 'me/me.html', locals())
