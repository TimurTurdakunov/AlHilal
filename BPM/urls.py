"""BPM URL Configuration

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
from django.urls import path
from rest_framework import routers
from directories.views import *
from processes.views import *
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)
router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_kato1/', KatoRegionsView.as_view()),
    path('get_kato2/', KatoDistrictView.as_view()),
    path('get_kato3/', KatoCommunityView.as_view()),
    path('get_country/', CountryView.as_view()),
    path('get_card_type/', CardTypeView.as_view()),
    path('get_tariff_plan/', TariffPlanView.as_view()),
    path('create_employee/', CustomUserView.as_view()),
    path('create_employee/<int:pk>', CustomUserView.as_view()),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain'),
    path('activate_account/<int:user_id>', activate_account_view),
    path('client/', ClientFormView.as_view()),
    path('client/<int:pk>', ClientFormDetailView.as_view()),
    path('get_kato1/<int:pk>', KatoRegionsView.as_view()),
    path('get_kato2/<int:pk>', KatoDistrictView.as_view()),
    path('get_kato3/<int:pk>', KatoCommunityView.as_view()),
]
