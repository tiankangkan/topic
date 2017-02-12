from __future__ import unicode_literals

from django.db import models

# Create your models here.


class PinType(object):
    PIN_TYPE_IMAGE = 'PIN_TYPE_IMAGE'
    PIN_TYPE_ARTICLE = 'PIN_TYPE_ARTICLE'
    PIN_TYPE_AUDIO = 'PIN_TYPE_AUDIO'
    PIN_TYPE_VIDEO = 'PIN_TYPE_VIDEO'
    PIN_TYPE_KM_ASK = 'PIN_TYPE_KM_ASK'


class PinBase(models.Model):
    id = models.AutoField(primary_key=True, default=0)
    pin_type = models.CharField(max_length=32, db_index=True, db_column="pin_type", default=PinType.PIN_TYPE_ARTICLE)
    title = models.CharField(max_length=256, db_index=True, db_column="title", default="")
    summary = models.CharField(max_length=1024, db_index=True, db_column="summary", blank=True, null=True)
    link = models.TextField(db_column="link", blank=True, null=True)
    labels = models.CharField(max_length=1024, db_column="labels", blank=True, null=True)
    image_url = models.TextField(db_column="image_url", blank=True, null=True)
    author = models.CharField(max_length=128, db_column="author", blank=True, null=True)
    time = models.DateTimeField(db_column="time", blank=True, null=True)
    extra_info = models.TextField(db_column="extra_info", blank=True, null=True)

    class Meta:
        abstract = True


class Pin(PinBase):
    class Meta:
        db_table = 'pin'


class PinKMAsk(PinBase):
    intro_info = models.TextField(db_column="intro_info", blank=True, null=True)
    times = models.TextField(db_column="times", blank=True, null=True)

    class Meta:
        db_table = 'pin_km_ask'
