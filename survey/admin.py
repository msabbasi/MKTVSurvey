# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Survey, Question, ChoiceGroup, Choice, Submission, Answer

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class ChoiceGroupAdmin(admin.ModelAdmin):
    #fieldsets = [
    #    (None,               {'fields': ['question_text']}),
    #    ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    #]
    inlines = [ChoiceInline]

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3

class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

class SubmissionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(ChoiceGroup, ChoiceGroupAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Submission, SubmissionAdmin)