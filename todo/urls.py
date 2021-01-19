from django.urls import path
from . import views
urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('<int:pk>/', views.todo_detail, name='todo_detail'),
    path('add/', views.todo_add, name='todo_add'),
    path('<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    path('logout/complete/', views.logout_complete, name='logout_complete'),
    path('<int:pk>/complete/', views.todo_complete, name='todo_complete'),
    path('searchresult/', views.search_result, name='search_result'),
    path('<int:pk>/delete/', views.todo_delete, name='todo_delete'),
]