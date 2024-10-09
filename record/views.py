from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from record.models import Record

# Create your views here.
def create(request):
    if request.method == 'POST':
        inputs = request.POST
        record = Record(first_name=inputs['first_name'], last_name=inputs['last_name'], role=inputs['role'], email=inputs['email'], user=request.user)
        record.save()
        return HttpResponseRedirect(reverse('record', kwargs={'id': record.id}))
    else:
        return render(request, 'create_record.html', {})

def records(request):
    records = Record.objects.filter(user=request.user)
    return render(request, 'records.html', {
        'records': records
    })


def record(request, id):
    record = Record.objects.get(pk=id)
    return render(request, 'record.html', {
        'record': record
    })

def edit_record(request, id): 
    inputs = request.POST
    record = Record(id=id, first_name=inputs['first_name'], last_name=inputs['last_name'], role=inputs['role'], email=inputs['email'], user=request.user)
    record.save()
    return HttpResponseRedirect(reverse('record', kwargs={'id': record.id}))

def delete_record(request, id):
    record = Record.objects.get(pk=id)
    record.delete()
    return HttpResponseRedirect(request.GET['next'])