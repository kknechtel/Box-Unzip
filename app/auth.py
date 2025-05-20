from flask import session, url_for, redirect, request, current_app
from boxsdk import OAuth2, Client
import uuid


def get_oauth():
    """Create and return a Box OAuth2 object"""
    return OAuth2(
        client_id=current_app.config['BOX_CLIENT_ID'],
        client_secret=current_app.config['BOX_CLIENT_SECRET']
    )


def get_authorization_url():
    """Generate Box authorization URL and CSRF token"""
    oauth = get_oauth()
    redirect_uri = current_app.config['BOX_REDIRECT_URI']
    csrf_token = str(uuid.uuid4())
    auth_url, _ = oauth.get_authorization_url(redirect_uri, csrf_token)
    session['oauth2_csrf_token'] = csrf_token
    return auth_url


def authenticate(auth_code):
    """Exchange auth code for tokens and store in session"""
    oauth = get_oauth()
    access_token, refresh_token = oauth.authenticate(auth_code)
    session['access_token'] = access_token
    session['refresh_token'] = refresh_token
    return access_token, refresh_token


def get_client():
    """Get authenticated Box client or redirect to auth"""
    if 'access_token' not in session:
        return None

    oauth = OAuth2(
        client_id=current_app.config['BOX_CLIENT_ID'],
        client_secret=current_app.config['BOX_CLIENT_SECRET'],
        access_token=session['access_token'],
        refresh_token=session.get('refresh_token')
    )

    def token_refreshed(access_token, refresh_token):
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token

    oauth.refresh_callback = token_refreshed
    return Client(oauth)

