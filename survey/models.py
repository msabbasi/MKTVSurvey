# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Survey(models.Model):
    name = models.CharField(max_length=50)
    #header_image_url = 
    #page_title = models.CharField(max_length=50)
    #description = models.CharField(max_length=200)

    @property
    def questions(self):
        return Question.objects.filter(survey = self.pk)

    def __str__(self):
        return self.name

class Submission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=50)
    sub_date = models.DateTimeField('date submitted', default=timezone.now)

    def __str__(self):
        return self.username

class ChoiceGroup(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Choice(models.Model):
    choice_group = models.ForeignKey(ChoiceGroup, on_delete=models.CASCADE)
    text_value = models.CharField(max_length=200)
    numeric_value = models.IntegerField(null=True, blank=True)
    
    OTHER = -1
    NORMAL = 0

    Type = (
        (OTHER, 'other'),
        (NORMAL, 'normal'),
    )

    choice_type = models.IntegerField(choices=Type, default=NORMAL)

    def __str__(self):
        return self.text_value

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    choice_group = models.ForeignKey(ChoiceGroup, on_delete=models.SET_NULL, null=True)
    required = models.BooleanField()
    text = models.CharField(max_length=200)

    RADIO = -1
    CHECKBOX = 0

    Type = (
        (RADIO, 'radio'),
        (CHECKBOX, 'checkbox'),
    )

    options_type = models.IntegerField(choices=Type, default=RADIO)

    @property
    def choices(self):
        return Choice.objects.filter(choice_group = self.choice_group)


    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    submission = models.ForeignKey(Survey, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.PROTECT)
    text = models.CharField(max_length=200, null=True, blank=True)
