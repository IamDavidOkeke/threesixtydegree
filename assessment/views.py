from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Assessment

# Create your views here.
def view_evaluator(request, id):
    ev = Assessment.objects.get(pk=id)
    if ev.survey.user == request.user:
        return render(request, 'view_evaluator.html', {
            'evaluator': ev
        })
    else:
        return HttpResponse('an error occured: You have no permission to access page')

def edit_evaluator(request, id): 
    ev = Assessment.objects.get(pk=id)
    ev.evaluator_name = request.POST['name']
    ev.evaluator_email = request.POST['email']
    ev.evaluator_relationship = request.POST['rel']
    ev.save()
    return HttpResponseRedirect(reverse('view_evaluator', kwargs={'id': ev.id}))

def delete_evaluator(request, id):
    ev = Assessment.objects.get(pk=id)
    ev.delete()
    return HttpResponseRedirect(request.GET['next'])