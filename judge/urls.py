from django.urls import path
from judge.views import (
    HomeView,
    NameDOBCreateView, 
    NameDOBUpdateView,
    ChangeFormatCreateView,
    ChangeFormatUpdateView,
    CropImageCreateView,
    CropImageUpdateView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create-name-dob/', NameDOBCreateView.as_view(), name='create_name_dob'),
    path('update-name-dob/<slug:id>/', NameDOBUpdateView.as_view(), name='update_name_dob'),

    path('change-format/', ChangeFormatCreateView.as_view(), name='change_format'),
    path('update-format/<slug:id>/', ChangeFormatUpdateView.as_view(), name='update_format'),

    path('crop-image/', CropImageCreateView.as_view(), name='crop_image'),
    path('update-crop-image/<slug:id>/', CropImageUpdateView.as_view(), name='update_crop_image'),

]
