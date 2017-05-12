# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.core.mail import send_mail
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
from django.utils import timezone

from .models import Survey, Question, ChoiceGroup, Answer, Submission

# Create your views here.

def submit(request):

    context = {
        'message': 'Thank you for your input!',
    }
    return render(request, 'survey/submit.html', context)

# Temporary implementation to obtain survey url
# Depending on how it needs to be interfaced with the website
# this implementation will be changed
def generate(request, survey_id):
    if request.method == 'GET':
        try:
            survey = get_object_or_404(Survey, pk=survey_id)
        except:
            raise Http404("Sorry, this survey does not exist")
        new_submission = Submission(survey=survey)

        new_submission.save()

        return HttpResponseRedirect(reverse('survey:survey_form', kwargs={'survey_id': str(survey.id)}) + "?usertoken=" + str(new_submission.id))
    else:
        raise SuspiciousOperation("404 Bad Request")

def survey_form(request, survey_id):

    try:
        survey = get_object_or_404(Survey, pk=survey_id)
    except:
        raise Http404("Sorry, this survey does not exist")

    if request.method == 'POST':
        username = request.POST.get('usertoken')
        if username == None:
            raise SuspiciousOperation("400 Bad Request")

        try:
            submission = get_object_or_404(Submission, pk=username)
        except:
            raise PermissionDenied("Sorry, you don't have access to this survey")

        if (submission.sub_date != None):
            raise PermissionDenied("This survey has already been filled out")

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
                print(request.POST.get(q.id))
                choice = q.choices.get(pk=request.POST[str(q.id)])
                a = Answer(submission=submission, question=q, choice=choice)
                if choice.choice_type == choice.OTHER:
                    other_text = request.POST[str(q.id)+"-other"]
                    a.other_text=other_text
                    submission_str += other_text+"\n"
                else:
                    submission_str += choice.text_value+"\n"
                a.save()
                try:
                    u = 5
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
        
        submission.sub_date = timezone.now()
        submission.save()
        print(submission_str)
        email_subject = "New submission: " + survey.name
        

        send_mail(
            email_subject,
            submission_str,
            'mujdasaood@gmail.com',
            ['mujdasaood@gmail.com'],
            fail_silently=False,
        )

        return HttpResponseRedirect(reverse('survey:submit')+'?usertoken='+str(submission.id))

    elif request.method == 'GET':
        username = request.GET.get('usertoken')
        if username == None:
            raise SuspiciousOperation("400 Bad Request")
        
        try:
            submission = get_object_or_404(Submission, pk=username)
        except:
            raise PermissionDenied("Sorry, you don't have access to this survey")

        if (submission.sub_date != None):
            raise PermissionDenied("This survey has already been filled out")

    return render(request, 'survey/survey_form.html', {'survey': survey, 'usertoken': username})



