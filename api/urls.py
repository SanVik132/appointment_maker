from django.urls import path,include

from api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'signup', views.SignUpViewSet)
router.register(r'login', views.LogInViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
