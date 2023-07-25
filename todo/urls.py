
from django.urls import path, include
from . import views

app_name = 'todo'

urlpatterns = [
        path('', views.index, name='index'),
        path('todo_list_partial', views.todo_list_partial, name='todo_list_partial'),
        path('todo_list_partial/<int:pk>', views.todo_details_partial, name='todo_details_partial'),
        path('create/', views.create, name='create'),
        path('rerank/', views.rerank, name='rerank',)
        ]
