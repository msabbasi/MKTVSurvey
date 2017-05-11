# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import loader, RequestContext
from django.core.mail import send_mail

from .models import Survey, Question, ChoiceGroup, Answer, Submission

# Create your views here.


# HTTP Error 404
def page_not_found(request):
    response = render_to_response(
    'submit.html',
    context_instance=RequestContext(request)
    )

    response.status_code = 404

    return response

def submit(request):

    context = {
        'message': 'Thank you for your input!',
    }
    return render(request, 'survey/submit.html', context)


def survey_form(request, survey_id):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            survey_id = request.POST.get('survey_id')
            survey = get_object_or_404(Survey, pk=survey_id)
        except:
            context = {
                'message': 'Survey not found!',
            }
            return render(request, 'survey/submit.html', context)

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

        context = {
            'message': 'Thank you for your input!',
        }

        return HttpResponseRedirect(reverse('survey:submit'))
    elif request.method == 'GET':
        survey = get_object_or_404(Survey, pk=survey_id)
        try:
            username = request.GET.get('username', '')
        except:
            context = {
                'message': 'Survey not found!',
            }
            return render(request, 'survey/submit.html', context)

    return render(request, 'survey/survey_form.html', {'survey': survey, 'username': username})



