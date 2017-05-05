from django.conf.urls import url

from . import views


app_name = 'survey'
urlpatterns = [
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^(?P<survey_id>[0-9]+)$', views.survey_form, name='survey_form'),
    ]
