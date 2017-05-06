# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail

from .models import Survey, Question, ChoiceGroup

# Create your views here.
def submit(request):
    survey_id = request.GET.get('SurveyID', '0')
    username = request.GET.get('username', '')
    context = {
        'username': username,
    }

    survey = get_object_or_404(Survey, pk=survey_id)

    questions = survey.questions

    for q in questions:
        selected_choice = q.choices.get(pk=request.POST['choice'])

    print(request.POST['choice'])
    
    #send_mail(
    #    'subject here',
    #    'message',
    #    'mujdasaood@gmail.com',
    #    ['mujdasaood@gmail.com'],
    #    fail_silently=False,
    #)
    return render(request, 'survey/submit.html', context)


def survey_form(request):
    survey_id = request.GET.get('SurveyID', '0')
    username = request.GET.get('username', '')
    survey = get_object_or_404(Survey, pk=survey_id)

    #select_template(['survey_%s_form.html' % survery_id])

    return render(request, 'survey/survey_form.html', {'survey': survey, 'username': username})



