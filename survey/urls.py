from django.conf.urls import url

from . import views


app_name = 'survey'

#handler400 = 'survey.views.bad_request'
#handler403 = 'survey.views.permission_denied'
#handler404 = 'views.page_not_found'
#handler500 = 'survey.views.server_error'


urlpatterns = [
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^generate/(?P<survey_id>[0-9]+)$', views.generate, name='generate'),
    #url(r'^$', views.survey_form, name='survey_form')
    url(r'^(?P<survey_id>[0-9]+)$', views.survey_form, name='survey_form'),
    ]



