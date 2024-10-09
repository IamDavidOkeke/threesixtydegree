from django.urls import path
from . import views

urlpatterns = [
    #form
    path('', views.create, name='form'),
    path('all', views.view_forms, name='view_forms'),
    path('<int:id>', views.view_form, name='view_form'),
    path('<int:id>/delete', views.delete_form, name='delete_form'),
    path('<int:id>/edit', views.edit_form, name='edit_form'),

    #section
    path('<int:id>/add_section', views.add_section, name='add_section'),
    path('section/<int:id>/edit', views.edit_section, name='edit_section'),
    path('section/<int:id>/delete', views.delete_section, name='delete_section'),
    path('<int:id>/edit_text_section', views.edit_text_section, name='edit_text_section'),

    #response
    path('<int:id>/r/<uuid:ev_id>', views.respond, name='respond'),
    path('r/<int:id>', views.view_response, name='response')
]