# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class Survey(models.Model):
    name = models.CharField(max_length=50)
    #header_image_url = 
    page_title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

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
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Choice(models.Model):
   
    OTHER = -1
    NORMAL = 0

    Type = (
        (OTHER, 'other'),
        (NORMAL, 'normal'),
    )

    choice_type = models.IntegerField(choices=Type, default=NORMAL)
    choice_group = models.ForeignKey(ChoiceGroup, on_delete=models.CASCADE)
    text_value = models.CharField(max_length=200)
    #numeric_value = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.text_value

class Question(models.Model):
    RADIO = -1
    CHECKBOX = 0
    SLIDER = 1
    DROPDOWN = 2
    TEXT = 3

    input_types = (
        (RADIO, 'radio'),
        (CHECKBOX, 'checkbox'),
        (SLIDER, 'slider'),
        (DROPDOWN, 'dropdown'),
        (TEXT, 'text'),
    )

    input_type = models.IntegerField(choices=input_types, default=RADIO)
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    choice_group = models.ForeignKey(ChoiceGroup, on_delete=models.SET_NULL, null=True, blank=True)
    required = models.BooleanField()
    text = models.CharField(max_length=200)
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)

    def clean(self):
        """
        Custom constraints
        """
        if self.input_type == self.SLIDER and self.min_value is None:
            raise ValidationError("Please specify the range.")
        if self.input_type == self.SLIDER and self.max_value is None:
            raise ValidationError("Please specify the range.")
        if (self.input_type in (self.RADIO, self.CHECKBOX, self.DROPDOWN) and self.choice_group is None):
            raise ValidationError("Please specify the group of choices.")

    @property
    def choices(self):
        if self.choice_group:
            return Choice.objects.filter(choice_group = self.choice_group)
        else:
            return None

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    submission = models.ForeignKey(Survey, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.PROTECT, null=True)
    text = models.CharField(max_length=200, null=True, blank=True)
    other_text = models.CharField(max_length=200, null=True, blank=True)
    range_value = models.IntegerField(default=0)

    #TODO: custom constraints
