from django.urls import path, include
from . import views

urlpatterns = [

]


urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.home, name='home'),
    path('', views.home_page, name = "home_page"),

    path('customers/', include(([
        path('', views.index, name='quiz_list'),
    ], 'lookspace_app'), namespace='customers')),

    path('partners/', include(([
        path('', views.space_details_subsriptions, name='quiz_change_list'),
        path('details', views.all_space_details, name='space_details'),
         path('edit/<int:id>', views.edit_space_details, name='edit_details'),
    ], 'lookspace_app'), namespace='partners')),

]