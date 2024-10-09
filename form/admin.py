from django.contrib import admin
from .models import Form, FormSection, InputField, Response

# Register your models here.
admin.site.register(Form)
admin.site.register(FormSection)
admin.site.register(InputField)
admin.site.register(Response)