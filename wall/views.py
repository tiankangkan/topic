# -*- coding:utf-8 -*-

import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt


class PinType(object):
    PIN_TYPE_IMAGE = 'PIN_TYPE_IMAGE'


def reply_to_pin_wall(request):
    return render(request, 'wall/pin_wall.html', locals())


@csrf_exempt
def reply_to_filter_pin(request):
    records = []
    for i in range(100):
        records.append(dict(
            pin_type=PinType.PIN_TYPE_IMAGE,
            title='this is a pin',
            summary=u'他有许多要说明的，但又没时间开长会，所以只好把一份长汇报削短成半小时的简介。\nHe had a lot to explain, and no time for more than a short meeting. Thus a lengthy briefing had to be telescoped into half an hour.',
            link='https://www.baidu.com/',
            image_url='/static/public-img/wall/174CEB88-44B1-4438-9604-7F06A7227476.png',
            width=3
        ))
    return HttpResponse(json.dumps({'status': 'ok', 'data': records}))
