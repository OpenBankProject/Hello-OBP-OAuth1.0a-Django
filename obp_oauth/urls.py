from django.conf.urls import patterns, url

from .views import IndexView, AuthorizationView, BankView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^authorize/$', AuthorizationView.as_view(), name='authorize'),
    url(r'^bank/$', BankView.as_view(), name='bank'),
)