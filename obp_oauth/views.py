# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import TemplateView

from requests_oauthlib import OAuth1Session



class IndexView(TemplateView):
    template_name = "obp_oauth/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        openbank = OAuth1Session(
            settings.OAUTH_CLIENT_KEY,
            client_secret=settings.OAUTH_CLIENT_SECRET,
            callback_uri=settings.OAUTH_CALLBACK_URI
        )

        fetch_response = openbank.fetch_request_token(settings.OAUTH_TOKEN_URL)
        authorization_url = openbank.authorization_url(settings.OAUTH_AUTHORIZATION_URL)

        self.request.session['oauth_token'] = fetch_response.get('oauth_token')
        self.request.session['oauth_secret'] = fetch_response.get('oauth_token_secret')
        self.request.session.modified = True

        context['authorization_url'] = authorization_url
        return context


class AuthorizationView(TemplateView):
    template_name = "obp_oauth/authorization.html"

    def get_context_data(self, **kwargs):
        context = super(AuthorizationView, self).get_context_data(**kwargs)

        context['session'] = self.request.session['oauth_token']


        openbank = OAuth1Session(
            settings.OAUTH_CLIENT_KEY,
            client_secret=settings.OAUTH_CLIENT_SECRET,
            resource_owner_key=self.request.session['oauth_token'],
            resource_owner_secret=self.request.session['oauth_secret']
        )

        openbank.parse_authorization_response(self.request.build_absolute_uri())

        openbank.fetch_access_token(settings.OAUTH_ACCESS_TOKEN_URL)

        private_bank_json = openbank.get("https://ulsterbank.openbankproject.com/obp/v1.2.1/banks/ulster/accounts/charity1/owner/transactions")

        context['private_bank_json'] = private_bank_json.json()
        return context
