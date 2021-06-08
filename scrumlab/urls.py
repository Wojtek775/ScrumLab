"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jedzonko import views
from jedzonko.views import IndexView, Add_recipe_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/', IndexView.as_view()),
    path('main/', views.main),
    path('', views.index),
    path('recipes/list/', views.recipes),
    path('index/', views.Landing_page.as_view()),
    path('recipe/<int:id>/', views.Recipe_details_view.as_view()),
    path('recipe/add/', Add_recipe_view.as_view()),
    path('recipe/modify/<int:id>/', views.Recipe_edit_view.as_view()),
    path('plan/list/', views.Schedule_list_view.as_view()),
    path('plan/<int:id>/details/', views.Schedule_details_view.as_view()),
    path('plan/<int:id>/modify/', views.Schedule_modify_view.as_view()),
    path('plan/add/', views.Add_schedule_view.as_view()),
    path('plan/add-recipe/', views.Recipe_to_plan_view.as_view()),
    path('search', views.search, name='search')
]



#komentarz
