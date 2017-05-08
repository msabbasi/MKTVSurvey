# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Survey, Question, ChoiceGroup, Choice, Submission, Answer

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(ChoiceGroup)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Answer)
