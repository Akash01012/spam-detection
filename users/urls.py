from django.urls import path
from .views import (
    RegisterView,
    ContactListView,
    SpamMarkView,
    SearchByNameView,
    SearchByPhoneView,
    APIVisit)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', APIVisit.as_view(), name='api-visit'),
    path('register/', RegisterView.as_view(), name='register'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('mark-spam/', SpamMarkView.as_view(), name='mark-spam'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search-by-name/', SearchByNameView.as_view(), name='search-by-name'),
    path('search-by-phone/', SearchByPhoneView.as_view(), name='search-by-phone'),
]
