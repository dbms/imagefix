from django.urls import path
import judge.views as views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create-name-dob/', views.NameDOBCreateView.as_view(), name='create_name_dob'),
    path('update-name-dob/<slug:uuid>/', views.NameDOBUpdateView.as_view(), name='update_name_dob'),

    path('change-format/', views.ChangeFormatCreateView.as_view(), name='change_format'),
    path('update-format/<slug:id>/', views.ChangeFormatUpdateView.as_view(), name='update_format'),

    path('crop-image/', views.CropImageCreateView.as_view(), name='crop_image'),
    path('update-crop-image/<slug:uuid>/', views.CropImageUpdateView.as_view(), name='update_crop_image'),

    path('resize-by-pixel/', views.ResizeByPixelCreateView.as_view(), name='resize_by_pixel'),
    path('resize-by-pixel/<slug:uuid>/', views.ResizeByPixelUpdateView.as_view(), name='update_resize_by_pixel'),

    path('compress-image/', views.CompressImageCreateView.as_view(), name='compress_image'),
    path('compress-image/<slug:uuid>/', views.CompressImageUpdateView.as_view(), name='update_compress_image'),

    path('image-to-pdf/', views.ImagePdfCreateView.as_view(), name='image_pdf'),

    path('contact-us/', views.ContactCreateView.as_view(), name='contact_us'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view()),


]
