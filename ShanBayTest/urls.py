"""ShanBayTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rewords import views as rewords_views
import settings

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', rewords_views.index),
    url(r'^login/', rewords_views.login),
    url(r'^accounts/auth/$',rewords_views.auth_view),
    url(r'^addNewNote/$',rewords_views.addNewNote),
    url(r'^setLearningPlan/$',rewords_views.setLearningPlan),
    url(r'^loadwordlist/$',rewords_views.loadwordlist),
    url(r'^learningList/$',rewords_views.learningList),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_ROOT }),
]


