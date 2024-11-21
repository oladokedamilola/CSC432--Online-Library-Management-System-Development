# users/urls.py

from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('onboarding/step1/', onboarding_step1, name='onboarding_step1'),
    path('onboarding/step2/', onboarding_step2, name='onboarding_step2'),
    path('onboarding/step3/', onboarding_step3, name='onboarding_step3'),


    path('dashboard/', user_dashboard, name='dashboard'),
    path('update_profile/', update_profile, name='update_profile'),

    
    path('login/', custom_login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]






# from django.urls import path
# from .views import *


# urlpatterns = [
#     # path('', reader_manage, name='reader_manage'),
#     # path('toggle-active/<int:pk>/', toggle_active, name='toggle_active'),
#     path('login/', librarian_login, name='librarian_login'),
#     path('dashboard/', librarian_dashboard, name='librarian_dashboard'),
#     # path('reader/edit/<int:pk>/', reader_edit, name='reader_edit'),

# ]
