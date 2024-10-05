"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from pulse.views.question_views import getAllQuestions



urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/getAllQuestions/', lambda request: get_all_questions_view(request), name='get_all_questions'),
    path('', include('pulse.urls.question_urls')),
    path('', include('pulse.urls')),
]

def get_all_questions_view(request):
    from pulse.views.question_views import getAllQuestions 
    return getAllQuestions(request)