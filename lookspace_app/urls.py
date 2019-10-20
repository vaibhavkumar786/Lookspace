from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    #  path('', views.index, name='index'),
    # path('', views.home, name='home'),
    # path('', views.home_page, name = "home_page"),

    path('customers/', include(([
        path('', views.all_unique_space, name='quiz_list'),
        path('booking/<int:id>', views.all_available_spaces, name='quiz_list'),
        path('availability/<int:id>', views.all_available_spaces, name='quiz_list'),

    ], 'lookspace_app'), namespace='customers')),

    path('partners/', include(([
        path('', views.space_details_subsriptions, name='quiz_change_list'),
        path('details', views.all_space_details, name='space_details'),
         path('edit/<int:id>', views.edit_space_details, name='edit_details'),
    ], 'lookspace_app'), namespace='partners')),

    path('', views.index, name = "index"),
    path('user_signup/', views.user_signup, name = "user_signup"),
    path('user_signin/', views.user_signin, name = "user_signin"),
    path('partner_signup/', views.partner_signup, name = "partner_signup"),
    path('partner_signin/', views.partner_signin, name = "partner_signin"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

