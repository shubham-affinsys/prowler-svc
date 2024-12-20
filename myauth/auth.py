import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, redirect, session, url_for, jsonify, flash
from authlib.integrations.base_client.errors import OAuthError
# Create a blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Load environment variables
oauth = OAuth()  # Initialize OAuth without passing the app yet

# Register Auth0 configuration
def configure_auth(app):
    global auth0  # Declare auth0 as global to access it in routes
    oauth.init_app(app)  # Now initialize OAuth with the main app
    auth0 = oauth.register(
        "auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
    )

# # Home route to check session or show login
# @auth_bp.route("/")
# def home():
#     if 'user' in session:
#         return jsonify({
#             "message": "Welcome",
#             "user_info": session['user']
#         })
#     else:
#         return jsonify({"message": "You need to log in"})

import secrets
# Auth0 Login
@auth_bp.route("/login")
def login():
    print("Attempting to log in...")
    nonce = secrets.token_urlsafe(16)  # Generate a secure random nonce
    session['nonce'] = nonce  # Store it in the session
    return auth0.authorize_redirect(redirect_uri=url_for("auth.callback", _external=True),nonce=nonce)

# auth callback
@auth_bp.route("/callback", methods=["GET", "POST"])
def callback():
    print("callback")
    try:
        token = auth0.authorize_access_token()  # Fetch the OAuth token
        nonce = session.pop('nonce', None)
        session["user"] = auth0.parse_id_token(token, nonce=nonce)  # Parse user info
        user_info = session["user"]
        # print(f"sesion details are: {session}")
        # Check if the user is blocked
        if user_info.get('blocked', False):
            print(f"user blocked : {user_info.get('blocked')}")
            flash('Your account has been blocked. Please contact support.', 'error')
            return redirect(url_for('auth.login'))
        
        #FIX : sensitive info may be logged
        # If the email domain
        print(f"User logged in successfully ,user info : {user_info}", flush=True)
        print(f"user token details: {token}")
        return redirect("/")  # Redirect to your dashboard
        # return redirect("https://prowler.bankbuddy.me")
    except Exception as e:
        print(f"OAuth error: {e}")
        flash('Authentication failed. Please try again.', 'error')
        return redirect(url_for('auth.login'))

# Auth0 Logout
@auth_bp.route("/logout")
def logout():
    user_info = session.get('user', None)
    #FIX : sensitive info may be logged
    print(f"Logging out user: {user_info}",flush=True)  # Print user info before logging out

    session.clear()
    print("user logged out redirecting to login page",flush=True)
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode({
            "returnTo": url_for("auth.login", _external=True),
            "client_id": env.get("AUTH0_CLIENT_ID"),
        }, quote_via=quote_plus)
    )

# API Route to check if the user is authenticated
@auth_bp.route("/api/check-session")
def check_session():
    if 'user' in session:
        return jsonify({"logged_in": True, "user": session['user']})
    return jsonify({"logged_in": False})
