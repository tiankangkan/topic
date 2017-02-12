# -*- coding: UTF-8 -*-

"""
Desc: django util.
Note:

---------------------------------------
# 2016/04/17   kangtian         created

"""
import json

from django import template
from django.db import models, connection, connections
from django.core.management import color
from django.conf import settings
from django.shortcuts import render
from django.template.defaulttags import register


def get_request_body(request, raw=None):
    """
    :param request:
    :param raw: raw = 'GET' | 'POST'
    :return:
    """

    body_dict = dict()
    if 'GET' == raw or 'POST' == raw:
        d = getattr(request, raw)
        if d:
            for key in d:
                body_dict[key] = d[key]
    else:
        if request.GET:
            for key in request.GET:
                body_dict[key] = request.GET[key]
        if request.POST:
            for key in request.POST:
                body_dict[key] = request.POST[key]
    return body_dict


def get_statements_create_table(database_name, model_obj):
    sql_create = connections[database_name].creation.sql_create_model
    style = color.no_style()
    cursor = connections[database_name].cursor()
    statements, references = sql_create(model_obj, style)
    return statements


def get_field_list_of_model(model):
    return [f.name for f in model._meta.get_fields() if not f.is_relation or f.one_to_one or (f.many_to_one and f.related_model)]


def render_html(request, template, context):
    context['DEPLOY_URL'] = settings.DEPLOYURL
    return render(request, template, context)


@register.filter('pretty_json')
def pretty_json(json_text):
    try:
        pretty_json_text = json.dumps(json_text, indent=4)
        return pretty_json_text
    except Exception:
        return json_text


@register.filter(name='one_more')
def one_more(_1, _2):
    return _1, _2


@register.filter(name='get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)


@register.filter(name='try_replace_with_dict')
def try_replace_with_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key, key)


@register.filter(name='default_if_none')
def default_if_none(obj, value):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    return obj if obj else value


@register.inclusion_tag('djutils/sort_th.html', takes_context=True)
def sort_th(context, sort_param_name, label):
    return {
        'is_current': context['sort_params'][sort_param_name]['is_current'],
        'is_reversed': context['sort_params'][sort_param_name]['is_reversed'],
        'url': context['sort_params'][sort_param_name]['url'],
        'label': label,
    }


if __name__ == "__main__":
    pass
