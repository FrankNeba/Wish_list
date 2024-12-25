from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home' ),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('addwish', views.add_item, name='addwish'),
    path('edit/<str:pk>', views.edit_item, name='edit'),
    path('delete/<str:pk>', views.delete_item, name='delete'),
    path('<str:username>', views.wishes, name='wish'),

]