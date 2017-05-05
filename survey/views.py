# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail

from .models import Survey, Question, ChoiceGroup

# Create your views here.
def submit(request):
    context = {
        'username': 'user',
    }
    send_mail(
        'subject here',
        'message',
        'mujdasaood@gmail.com',
        ['mujdasaood@gmail.com'],
        fail_silently=False,
    )
    return render(request, 'survey/submit.html', context)


def survey_form(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    questions = Question.objects.filter(survey_id = survey_id)

    choice_groups = {}

    for question in questions:
        choice_groups[question.choice_group_id] = ChoiceGroup.objects.get(pk = question.choice_group_id)

    return render(request, 'survey/survey_form.html', {'survey': survey, 'choicegroups': choice_groups})



