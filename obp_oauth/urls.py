from django.urls import path

from obp_oauth.views import IndexView, AuthorizationView, BankView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('authorize/', AuthorizationView.as_view(), name='authorize'),
    path('bank/', BankView.as_view(), name='bank'),
    ]
