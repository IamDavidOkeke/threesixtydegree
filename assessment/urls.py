from django.urls import path
from . import views


urlpatterns=[
    path('<uuid:id>', views.view_evaluator, name='view_evaluator'), 
    path('<uuid:id>/delete', views.delete_evaluator, name='delete_evaluator'),
    path('<uuid:id>/edit', views.edit_evaluator, name='edit_evaluator'),
]