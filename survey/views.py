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

    submission_str = ""

    questions = survey.questions
    for q in questions:

        submission_str += q.text+"\n"

        if q.input_type == q.SLIDER:
            range_value = int(request.POST[str(q.id)])
            a = Answer(submission=submission, question=q, range_value=range_value)
            a.save()
            submission_str += str(range_value)+"\n"
        elif q.input_type == q.DROPDOWN:
            choice = q.choices.get(pk=request.POST[str(q.id)])
            a = Answer(submission=submission, question=q, choice=choice)
            a.save()
            submission_str += choice.text_value+"\n"
        elif q.input_type == q.RADIO:
            try:
                choice = q.choices.get(pk=request.POST[q.id])
                a = Answer(submission=submission, question=q, choice=choice)
                if choice.choice_type == choice.OTHER:
                    other_text = request.POST[str(q.id)+"-other"]
                    a.other_text=other_text
                    submission_str += other_text+"\n"
                    #TODO: check if other text is filled
                else:
                    submission_str += choice.text_value+"\n"
                a.save()
            except:
                submission_str += "-\n"
        elif q.input_type == q.CHECKBOX:
            try:
                checked = request.POST.getlist(str(q.id))
                for each in checked:
                    choice = q.choices.get(pk=each)
                    a = Answer(submission=submission, question=q, choice=choice)
                    a.save()
                    submission_str += choice.text_value+"\n"
            except:
                submission_str += "-\n"
        elif q.input_type == q.TEXT:
            try:
                text = request.POST[str(q.id)]
                a = Answer(submission=submission, question=q, text=text)
                a.save()
                submission_str += text+"\n"
            except:
                submission_str += "-\n"

        submission_str += "\n"

    print(submission_str)
    email_subject = "New submission: " + survey.name
    
    #TODO: Nice string to send in email

    #send_mail(
    #    email_subject,
    #    submission_str,
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



