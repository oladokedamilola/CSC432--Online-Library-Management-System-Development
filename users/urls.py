from django.urls import path
from .views import *


urlpatterns = [
    path('', reader_manage, name='reader_manage'),
    path('toggle-active/<int:pk>/', toggle_active, name='toggle_active'),
    path('librarian/login/', librarian_login, name='librarian_login'),
    path('librarian/logout/', librarian_logout, name='librarian_logout'),
    path('librarian/dashboard/', librarian_dashboard, name='librarian_dashboard'),
    path('reader/edit/<int:pk>/', reader_edit, name='reader_edit'),

]
