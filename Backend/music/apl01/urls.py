from django.urls import path
from apl01 import views 
from apl01.views import temp,Signup
from apl01.views import sri,Signup
from apl01.views import sri,Login
from apl01.views import sri,Categories




urlpatterns = [
    path('',views.temp,name='temp'),
    path('signup',Signup.as_view(),name='signup'),
    path('login',Login.as_view(),name='login'),
    path('categories',Categories.as_view(),name='categories'),
    path('sri',views.sri,name='sri')
]