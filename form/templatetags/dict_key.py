from django import template

register = template.Library()

@register.filter()
def dict_key(arg1, arg2):
    scale = {
        '1':'Never',
        '2':'Seldom',
        '3':'Sometimes',
        '4':'Frequently',
        '5':'Always',
    }
    if str(arg2) in arg1:
        response = arg1[str(arg2)]
        return scale[f"{response}"]
    else:
        return 'No response'