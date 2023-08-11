from flask import redirect, request
from oauth_logic import begin_oauth, return_oauth

def register_routes(app):
    app.add_url_rule('/OAuth/begin_oauth', view_func=begin_oauth, methods=['GET'])
    app.add_url_rule('/OAuth/return_oauth', view_func=return_oauth, methods=['GET', 'POST'])
