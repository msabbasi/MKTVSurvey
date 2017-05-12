# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Survey, Question, ChoiceGroup, Choice, Submission, Answer

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    readonly_fields=('id',)

class ChoiceGroupAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    readonly_fields=('id',)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3
    readonly_fields=('id',)

class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    readonly_fields=('id',)

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields=('id',)

class SubmissionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    readonly_fields=('id',)


admin.site.register(ChoiceGroup, ChoiceGroupAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Submission, SubmissionAdmin)