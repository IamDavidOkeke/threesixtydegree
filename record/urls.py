from django.urls import path
from . import views

urlpatterns = [
    path('', views.create, name='create_record'),
    path('all/', views.records, name='records' ),
    path('<int:id>', views.record, name='record'),
    path('<int:id>/edit', views.edit_record, name='edit_record'),
    path('<int:id>/delete', views.delete_record, name='delete_record'),
]