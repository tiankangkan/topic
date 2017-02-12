# -*- coding:utf-8 -*-

import json
import traceback

from .models import PinType
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from db_adapter.models_adapter import ModelsAdapter


def reply_to_pin_wall(request):
    return render(request, 'wall/pin_wall.html', locals())


def reply_to_add_pin(request):
    return render(request, 'wall/add_pin.html', locals())


@csrf_exempt
def reply_to_filter_pin(request):
    try:
        records = []
        # for i in range(100):
        #     records.append(dict(
        #         pin_type=PinType.PIN_TYPE_IMAGE,
        #         title='this is a pin',
        #         summary=u'他有许多要说明的，但又没时间开长会，所以只好把一份长汇报削短成半小时的简介。\nHe had a lot to explain, and no time for more than a short meeting. Thus a lengthy briefing had to be telescoped into half an hour.',
        #         link='https://www.baidu.com/',
        #         image_url='/static/public-img/wall/174CEB88-44B1-4438-9604-7F06A7227476.png',
        #         width=3
        #     ))
        model = ModelsAdapter(table_name='wall.models.Pin')
        records = model.filter()
        for record in records:
            if record['pin_type'] == PinType.PIN_TYPE_ARTICLE:
                record['summary'] = record['summary'] if len(record['summary']) < 512 else record['summary'][:512] + '...'
                record['width'] = min(max(len(record['summary']) / 30, 2), 10)
        return HttpResponse(json.dumps({'status': 'ok', 'data': records}))
    except:
        return HttpResponse(json.dumps({'status': 'error', 'data': traceback.format_exc()}))


@csrf_exempt
def reply_to_submit_pin(request):
    try:
        values_json = request.POST.get('values')
        record = json.loads(values_json)
        model = ModelsAdapter(table_name='wall.models.Pin')
        model.insert(**record)
        return HttpResponse(json.dumps({'status': 'ok', 'data': 'ok'}))
    except:
        return HttpResponse(json.dumps({'status': 'error', 'data': traceback.format_exc()}))
