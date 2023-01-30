# from django.contrib import admin
from django.urls import path
from .views import About,Home,Contact,Index,Login,Logout_admin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', Home, name='home'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('admin_login/', Login, name='admin_login'),
    path('logout/', Logout_admin, name='logout_admin')
]
