from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name = "index"),
    path('user_signup/', views.user_signup, name = "user_signup"),
    path('user_signin/', views.user_signin, name = "user_signin"),
    path('partner_signup/', views.partner_signup, name = "partner_signup"),
    path('partner_signin/', views.partner_signin, name = "partner_signin"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)