from django.urls import path
from .views import FirstLoginView, FirstRegisterView, TodoCreate, TodoDelete, TodoList, TodoUpdate, TodoDetail
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TodoList.as_view(), name='todolist'),
    path('create/', TodoCreate.as_view(), name='todocreate'),
    path('tododetail/<int:pk>/', TodoDetail.as_view(), name='tododetail'),
    path('update/<int:pk>/', TodoUpdate.as_view(), name='todoupdate'),
    path('delete/<int:pk>/', TodoDelete.as_view(), name='tododelete'),

    path('login/', FirstLoginView.as_view(), name='login'),
    path('register/', FirstRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]


