# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import TemplateView
from requests_oauthlib import OAuth1Session


def get_oauth1(request):
    openbank_oauth1 = OAuth1Session(
        settings.OBP_OAUTH_CLIENT_KEY,
        client_secret=settings.OBP_OAUTH_CLIENT_SECRET,
        resource_owner_key=request.session['oauth_token'],
        resource_owner_secret=request.session['oauth_secret']
    )
    return openbank_oauth1


class IndexView(TemplateView):
    template_name = "obp_oauth/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        openbank = OAuth1Session(
            settings.OBP_OAUTH_CLIENT_KEY,
            client_secret=settings.OBP_OAUTH_CLIENT_SECRET,
            callback_uri=settings.OBP_OAUTH_CALLBACK_URI
        )

        # OBP_OAUTH1 Provider does not need to be with the Bank
        fetch_response = openbank.fetch_request_token(
            settings.OBP_OAUTH_TOKEN_URL)
        authorization_url = openbank.authorization_url(
            settings.OBP_OAUTH_AUTHORIZATION_URL)

        self.request.session['oauth_token'] = fetch_response.get('oauth_token')
        self.request.session['oauth_secret'] = fetch_response.get(
            'oauth_token_secret')
        self.request.session.modified = True

        context['authorization_url'] = authorization_url
        return context


class AuthorizationView(TemplateView):
    template_name = "obp_oauth/authorization.html"

    def get_context_data(self, **kwargs):
        context = super(AuthorizationView, self).get_context_data(**kwargs)

        openbank = OAuth1Session(
            settings.OBP_OAUTH_CLIENT_KEY,
            client_secret=settings.OBP_OAUTH_CLIENT_SECRET,
            resource_owner_key=self.request.session['oauth_token'],
            resource_owner_secret=self.request.session['oauth_secret']
        )

        openbank.parse_authorization_response(
            self.request.build_absolute_uri())

        fetch_response = openbank.fetch_access_token(
            settings.OBP_OAUTH_ACCESS_TOKEN_URL)

        self.request.session['oauth_token'] = fetch_response.get('oauth_token')
        self.request.session['oauth_secret'] = fetch_response.get(
            'oauth_token_secret')

        context['private_bank_json'] = fetch_response
        return context


class BankView(TemplateView):
    template_name = "obp_oauth/bank.html"

    def get_context_data(self, **kwargs):
        context = super(BankView, self).get_context_data(**kwargs)

        openbank_oauth1 = get_oauth1(self.request)

        # DEMO REQUEST TO GET ALL ACCOUNTS (CREATED AS EXAMPLE VIA THE UI)
        private_bank_json = openbank_oauth1.get(
            'https://demo.openbankproject.com/obp/v4.0.0/banks/dmo.02.de.de/accounts-held')
        context['private_bank_json'] = private_bank_json.json()

        return context
