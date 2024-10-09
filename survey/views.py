from django.core import serializers
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from form.models import Form
from assessment.models import Assessment
from survey.models import Survey
from record.models import Record
from assessment.helpers import email_body_template
from smtplib import SMTPException
import uuid
# Create your views here.

def create(request):
    if request.method == 'POST':
        form = Form.objects.get(pk=int(request.POST['form']))
        if 'email-template' in request.POST:
            survey = Survey(title=request.POST['title'], form=form, user=request.user, email_template=request.POST['email-template'])
        else:
            survey = Survey(title=request.POST['title'], form=form, user=request.user)
        survey.save()
        return HttpResponseRedirect(reverse('view_survey', kwargs={'id': survey.id}))
    else:
        forms = Form.objects.filter(user=request.user)
        return render(request, 'create_survey.html', {
            'forms': forms,
            'email_template':email_body_template
        })

def view_surveys(request):
    surveys = Survey.objects.filter(user=request.user)
    return render(request, 'view_surveys.html', {
        "surveys": surveys
    })

def view_survey(request, id):
    survey = Survey.objects.get(pk=id)
    non_survey_records = Record.objects.filter(user=request.user).exclude(survey=survey)
    if survey.user == request.user:
        return render(request, 'survey.html', {
            'survey': survey,
            'non_survey_records':non_survey_records
        })
    else:
        return HttpResponse('an error occured: You have no permission to access page')

def create_record(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'create_record.html', {})

def add_record(request, id):
    if request.method == 'POST':
        inputs = request.POST
        survey = Survey.objects.get(pk=id)
        if request.GET['type'] == 'new':
            record = Record(first_name=inputs['first_name'], last_name=inputs['last_name'], role=inputs['role'], email=inputs['email'], user=request.user)
            record.save()
        elif request.GET['type'] == 'existing':
            record = Record.objects.get(pk=inputs['record_id'])
        record.survey.add(survey)
        data = serializers.serialize('json', [record], fields=('id', 'first_name', 'last_name','role', 'email'))
        return HttpResponse(data, content_type='application/json')
    else:
        return render(request, 'add_record.html', {})
    
def delete_survey_record(request, s_id, r_id):
    record = Record.objects.get(pk=r_id)
    survey = record.survey.get(pk=s_id) 
    if survey.user == request.user:
        record.survey.remove(survey)
        return HttpResponseRedirect(reverse('view_survey', kwargs={'id': survey.id}))
    else:
       return HttpResponse('an error occured: You have no permission to access page')

def view_survey_record(request, s_id, r_id):
    record = Record.objects.get(pk=r_id)
    survey = record.survey.get(pk=s_id) 
    ev = record.assessment_set.filter(survey=survey)
    if survey.user == request.user:
        return render(request, 'view_survey_record.html', {
        'survey': survey,
        'record': record,
        'ev': ev
    })
    else:
       return HttpResponse('an error occured: You have no permission to access page')

def add_evaluator(request, s_id, r_id):
    inputs = request.POST
    record = Record.objects.get(pk=r_id)
    survey = record.survey.get(pk=s_id)
    a = Assessment(id=uuid.uuid4(), evaluator_name=inputs['name'], evaluator_email=inputs['email'], evaluator_relationship=inputs['rel'], survey=survey, record=record)
    try:
        a.save()
        print(request.build_absolute_uri(reverse('respond', kwargs={'id': survey.form.id, 'ev_id':a.id})))
    except SMTPException as e:
        print(e)
        return HttpResponse([{'msg': 'error sending mail'}], content_type='application/json')   
    a.save()
    data = serializers.serialize('json', [a], fields=('id', 'evaluator_name', 'evaluator_email','evaluator_relationship'))
    return HttpResponse(data, content_type='application/json')


def view_summary(request, s_id, r_id):
    record = Record.objects.get(pk=r_id)
    survey = record.survey.get(pk=s_id) 
    ev = record.assessment_set.filter(survey=survey)
    fields = {}
    for i in ev:
        for j in i.response.fields:
            if j in fields:
                fields[j]+= int(i.response.fields[j])
            else: 
                fields[j] = int(i.response.fields[j])
    sorted_fields = sorted(fields.items(), key=lambda x: x[1], reverse=True)
    if survey.user == request.user:
        return render(request, 'summary_report.html', {
        'survey': survey,
        'record': record,
        'ev': ev,
        'hi_ratings':sorted_fields[:2],
        'low_ratings': reversed(sorted_fields[-2:]),
    })
    else:
       return HttpResponse('an error occured: You have no permission to access page')