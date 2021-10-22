from django.contrib import admin
from django.urls import path
from blog_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('contract/', views.contract, name="contract"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('signup/', views.sign_up, name="signup"),
    path('addpost/', views.post_add, name="addpost"),
    path('update/<int:id>', views.post_update, name="update"),
    path('delete/<int:id>', views.post_delete, name="delete"),
]
