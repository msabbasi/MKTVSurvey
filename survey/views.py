# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail

from .models import Survey, Question, ChoiceGroup, Answer, Submission

# Create your views here.
def submit(request):
    print(request.POST)
    survey_id = request.POST.get('survey_id', '0')
    username = request.POST.get('username', '')
    context = {
        'username': username,
    }

    survey = get_object_or_404(Survey, pk=survey_id)
    submission = Submission(
                survey = survey,
                username = username)
    submission.save()

    questions = survey.questions
    for q in questions:
        choice = None
        text = None
        other_text = None
        range_value = None

        if q.input_type == q.SLIDER:
            range_value = int(request.POST[str(q.id)])
            a = Answer(submission=submission, question=q, range_value=range_value)
            a.save()
        elif q.input_type in (q.RADIO, q.DROPDOWN):
            choice = q.choices.get(pk=request.POST[str(q.id)])
            a = Answer(submission=submission, question=q, choice=choice)
            a.save()
        elif q.input_type == q.CHECKBOX:
            checked = request.POST[str(q.id)]
            for each in checked:
                choice = q.choices.get(pk=each)
                a = Answer(submission=submission, question=q, choice=choice)
                a.save()
        elif q.input_type == q.TEXT:
            text = request.POST[str(q.id)]
            a = Answer(submission=submission, question=q, text=text)
            a.save()

    print(request.POST)
    
    #send_mail(
    #    'subject here',
    #    'message',
    #    'mujdasaood@gmail.com',
    #    ['mujdasaood@gmail.com'],
    #    fail_silently=False,
    #)
    return render(request, 'survey/submit.html', context)


def survey_form(request):
    survey_id = request.GET.get('SurveyID')
    print(request.GET)
    print(survey_id)
    username = request.GET.get('username', '')
    survey = get_object_or_404(Survey, pk=survey_id)

    #select_template(['survey_%s_form.html' % survery_id])

    return render(request, 'survey/survey_form.html', {'survey': survey, 'username': username})



