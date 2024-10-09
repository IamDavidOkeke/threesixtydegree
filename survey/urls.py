from django.urls import path
from . import views

urlpatterns = [
    path('', views.create, name='survey'),
    path('all', views.view_surveys, name='view_surveys'),
    path('<int:id>', views.view_survey, name='view_survey'),
    path('<int:s_id>/record/<int:r_id>', views.view_survey_record, name='view_survey_record'),
    path('<int:s_id>/record/<int:r_id>/delete', views.delete_survey_record, name='delete_survey_record'),
    path('<int:s_id>/record/<int:r_id>/summary', views.view_summary, name='view_summary'),
    path('<int:id>/add_record', views.add_record, name='add_record'),
    path('<int:s_id>/record/<int:r_id>/add', views.add_evaluator, name='add_evaluator')
]