# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Survey(models.Model):
    name = models.CharField(max_length=50)

class Submission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50)
    sub_date = models.DateTimeField('date submitted',default=timezone.now)

class ChoiceGroup(models.Model):
    name = models.CharField(max_length=50)

class Choice(models.Model):
    choice_group = models.ForeignKey(ChoiceGroup, on_delete=models.CASCADE)
    text_value = models.CharField(max_length=200)
    numeric_value = models.IntegerField(null=True, blank=True)

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    choice_group = models.ForeignKey(ChoiceGroup, on_delete=models.SET_NULL, null=True)
    required = models.BooleanField()
    text = models.CharField(max_length=200)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    submission = models.ForeignKey(Survey, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.PROTECT)
    text = models.CharField(max_length=200, null=True, blank=True)
