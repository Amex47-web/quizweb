from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
from flask import session, redirect, request, url_for
import os

# Initialize Google OAuth2 Flow
client_secrets_file = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
flow = Flow.from_client_secrets_file(
    client_secrets_file,
    scopes=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email"
    ],
    redirect_uri="http://localhost:5000/auth/callback"
)

def get_google_login_url():
    """Initiate the Google OAuth2 flow and return the login URL."""
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return authorization_url

def handle_google_callback():
    """Handle the callback after user authorizes via Google."""
    if request.args.get('state') != session.get('state'):
        print("State mismatch detected!")
        return redirect(url_for('home'))

    # Fetch token and user info
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = google.auth.transport.requests.Request()

    # Get user info
    id_info = id_token.verify_oauth2_token(
        credentials.id_token, request_session, credentials.client_id
    )

    # Save user info to session
    print("before saving user info")
    session['user_email'] = id_info.get("email")
    session['user_name'] = id_info.get("name")
    print("email",session['user_email'])
