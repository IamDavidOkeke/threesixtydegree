from django import template
from form.models import InputField, TextFieldResponse

register = template.Library()

@register.filter()
def func(section, fields):
    sum = 0
    count = 0
    for q in section.inputfield_set.all():
        count += 1
        if str(q.id) in fields:
            sum += int(fields[str(q.id)])
    avg = round(sum/count,1)
    return avg

@register.filter()
def find_key(arg1, arg2):
    if str(arg2) in arg1:
        return arg1[str(arg2)]
    else:
        return ''


@register.filter()
def find_question(id):
    question = InputField.objects.get(pk=id)
    return question.label

@register.filter()
def get_text_response(r_id, q_id):
    response = TextFieldResponse.objects.get(response__id=r_id, question__id=q_id)
    return response.answer