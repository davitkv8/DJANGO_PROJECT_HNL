"""hirenlearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
import django.contrib.auth.urls as urls
from django.conf import settings
from django.conf.urls.static import static


from blog.views import main_view

from users.views import register,\
    complete_user_registration,\
    UpdateTeacherProfileView,\
    VerificationView,\
    lectures_detailed,\
    relationships,\
    search_result

from classroom.views import classroom, chat_room, AjaxTimeTable, redirecter, requested_table

urlpatterns = [
    path('admin/', admin.site.urls),

    # BLOG APP
    path('', main_view, name='main-view'),

    # USERS APP
    path('verify-user/<uidb64>/<token>/', VerificationView.as_view(), name='verification-view'),
    path('teacher/profile/<int:pk>/', UpdateTeacherProfileView.as_view(), name='teacher-profile'),
    path('teacher/<str:subject>/<int:pk>/', lectures_detailed, name='lectures-detailed'),
    path('complete/profile/<int:pk>/', complete_user_registration, name='complete-user'),
    re_path(r'^search/subject-(?P<subject>[A-Z-a-z]+)/min_price-(?P<min_price>[0-9]+)/'
            r'max_price-(?P<max_price>[0-9]+)/rating_from-(?P<rating>[0-9-a-z]+)/$',
            search_result, name='search_result'),
    path('requests/', relationships, name='relationships'),
    path('register/', register, name='register'),
    path('', include(urls)),

    # CLASSROOM APP
    path('redirect/<str:student>/<str:lecturer>/', redirecter, name='redirecter'),
    path('classroom/', classroom, name='classroom'),
    path('classroom/chat/<str:room_name>/', chat_room, name='chat_room'),
    re_path(r'^time_table/(?P<user_pk>[0-9]+)/$', AjaxTimeTable.as_view(), name="time_table"),
    path('classroom/<str:student_user>/<str:teacher_user>/', requested_table, name="requested_table")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
