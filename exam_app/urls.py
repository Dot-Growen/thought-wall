from django.urls import path
from . import views

urlpatterns = [
    # GET REQUEST
    path('', views.index),
    path('logout', views.logout),
    # PAGES
    path('thoughts', views.thought_page),
    path('thoughts/<int:id>', views.detail_page),
    # BUTTONs
    path('delete/<int:id>', views.delete),
    path('like/<int:id>', views.like),
    path('unlike/<int:id>', views.unlike),
    # POST REQUEST
    path('login', views.login), 
    path('register', views.register), 
    path('add', views.add),
]