import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, redirect, session, url_for, jsonify

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

# Auth0 Callback
@auth_bp.route("/callback", methods=["GET", "POST"])
def callback():
    print("callback")
    token = auth0.authorize_access_token()
    nonce = session.pop('nonce', None)
    session["user"] = auth0.parse_id_token(token, nonce=nonce)
    user = json.dumps(session["user"])

    #FIX : sensitive info may be logged
    print(f"User information after login:{user}",flush=True)
    print(f"acces token is:{token}",flush=True)

    return redirect("/")  # Redirect to your dashboard home
    # return redirect("https://prowler.bankbuddy.me")

# Auth0 Logout
@auth_bp.route("/logout")
def logout():
    user_info = session.get('user', None)
    #FIX : sensitive info may be logged
    print(f"Logging out user: {user_info}",flush=True)  # Print user info before logging out

    session.clear()
    print("logout",flush=True)
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
