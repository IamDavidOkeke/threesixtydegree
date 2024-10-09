from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Form, FormSection, InputField, Response, InputTextField, TextFieldResponse
from assessment.models import Assessment

# Create your views here.
def create(request):
    if request.method == 'POST':
        form = Form(name=request.POST['name'], description=request.POST['description'], user=request.user)
        form.save()
        return HttpResponseRedirect(reverse('edit_form', kwargs={'id':form.id}))
    else:
        return render(request, 'create.html', {})

def view_forms(request):
    forms = Form.objects.filter(user=request.user)
    return render(request, 'forms.html', {
        "forms": forms
    })

def view_form(request, id):
    form = Form.objects.get(pk=id)
    if form.user == request.user:
        return render(request, 'form.html', {
            "form": form
        })
    else:
        return HttpResponse('an error occured: You have no permission to access page')

def edit_form(request, id):
    form = Form.objects.get(pk=id)
    if form.user == request.user:
        if request.method == 'POST':
            form = Form(id=id, name=request.POST['name'], description=request.POST['description'], user=request.user)
            form.save()
            return HttpResponseRedirect(reverse('view_form', kwargs={'id': form.id}))
        else:
            return render(request, 'edit-form.html', {
                'form':form
            })
    else:
        return HttpResponse('an error occured: You have no permission to access page')
    
def delete_form(request, id):
    form = Form.objects.get(pk=id)
    if form.user == request.user:
        form.delete()
        return render(request, 'form-delete-success.html', {
        })
    else:
        return HttpResponse('an error occured: You have no permission to access page')
    
def respond(request, id, ev_id):
    form = Form.objects.get(pk=id)
    assessment = Assessment.objects.get(pk=ev_id)
    try:
        if assessment.response:
            return render(request, 'thanks-for-responding.html', { "response" :assessment.response})
    except:
        pass 
    if request.method == 'GET':
        return render(request, 'respond.html', { "form": form,"assessment" : assessment})
    else:
        fields = {}
        for s in form.formsection_set.all():
            for q in s.inputfield_set.all():
                fields[str(q.id)] = request.POST.get(str(q.id))
        response = Response(form=form, assessment=assessment, fields=fields)
        response.save()
        for q in form.inputtextfield_set.all():
            text_response = TextFieldResponse(question=q, answer=request.POST.get(f"text-{q.id}"), response=response)
            text_response.save()
        return render(request, 'thanks-for-responding.html', { "response" :response})
        

def view_response(request, id):
    response = Response.objects.get(pk=id)
    if response is None:
        return render(request, 'form.html', {"form": form })
    else: 
        form = response.form
        return render(request, 'view_response.html', {"form": form, "response": response})

def add_section(request, id):
    form = Form.objects.get(pk=id)
    section = FormSection(name=request.POST['name'], form=form)
    section.save()
    for n in request.POST:
        if n.startswith('question'):
            n = InputField(label=request.POST[n], section=section)
            n.save()
    return HttpResponseRedirect(reverse('edit_form', kwargs={'id': form.id}))


def edit_section(request, id):
    section = FormSection.objects.get(pk=id)
    section.name = request.POST['name']
    section.save()
    for q in section.inputfield_set.all():
        if str(q.id) not in request.POST:
            q.delete()
        else:
            old = InputField(id=q.id, label=request.POST[str(q.id)], section=section)
            old.save()
    for n in request.POST:
        if n.startswith('question'):
            n = InputField(label=request.POST[n], section=section)
            n.save()
    return HttpResponseRedirect(reverse('edit_form', kwargs={'id': section.form.id}))
    
def delete_section(request, id):
    section = FormSection.objects.get(pk=id)
    form = section.form
    section.delete()
    return HttpResponseRedirect(reverse('edit_form', kwargs={'id': form.id}))

def edit_text_section(request, id):
    form = Form.objects.get(pk=id)
    for q in form.inputtextfield_set.all():
        if str(q.id) not in request.POST:
            q.delete()
        else:
            old = InputTextField(id=q.id, label=request.POST[str(q.id)], form=form)
            old.save()
    for i in request.POST:
        if i.startswith('question'):
            question = InputTextField(label=request.POST[str(i)], form=form)
            question.save()
    return HttpResponseRedirect(reverse('edit_form', kwargs={'id': form.id}))