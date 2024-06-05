"""
URL configuration for bank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login),
    path('register', views.userregistration, name="register"),
    path('withdrawal', views.withdraw),

    path('bankregister', views.adminoptions),
    path('bankprofile', views.bankprofile),
    path('Deposit', views.deposit),
    path('enquiry', views.balance),
    path('userhome', views.userhome),
    path('more', views.usermore),
    path('back', views.back),
    path('count', views.usercount),
    path('viewusers', views.all_users),
    path('user_view/<int:id>', views.user_view, name="user_view"),
    path('viewhistory', views.history),
    path('bankhistory/<int:id>', views.bankhistory, name="bankhistory"),
    path('edituser', views.edit),
    path('logout', views.log_out, name="logout"),
    path('Search', views.search),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)