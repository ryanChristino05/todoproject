from django.urls import path
from .import views
app_name="tasks"
urlpatterns=[
    path('',views.task_list,name='task_list'),
    path('add/',views.add_task,name='add_task'),
    path('delete/<int:task_id>/',views.delete_task,name="delete_task"),
    path('modifier-taches/<int:task_id>/',views.edit_task,name="edit_task")
]