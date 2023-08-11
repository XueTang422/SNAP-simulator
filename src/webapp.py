import logging

import requests

from flask import Flask, render_template, redirect, request

log = logging.getLogger(__name__)

app = Flask(__name__)

secret_vars = {
    'client_id': '77z6jwn2wdkrg3',
    'client_secret': 'FjZsrETXwqEEQqTS',
    'state_secret': 'test',
}

@app.route('/')
def index():
    return render_template('snap_display_widget_playground.html')


@app.route('/OAuth/begin_oauth', methods=['GET'])
def begin_oauth():
    return redirect("https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id="
                    + secret_vars['client_id'] + "&redirect_uri=http://xuetangtest.pythonanywhere.com/OAuth/return_oauth&state="
                    + secret_vars['state_secret'] + "&scope=r_sales_nav_display")


@app.route('/OAuth/return_oauth', methods=['GET', 'POST'])
def return_oauth():
    AT_result = {}
    code = request.args.get('code', default='Not available', type=str)
    params = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': secret_vars['client_id'],
        'client_secret': secret_vars['client_secret'],
        'scope': 'r_sales_nav_display',
        'redirect_uri': 'http://xuetangtest.pythonanywhere.com/OAuth/return_oauth',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    try:
        response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            api_response = response.json()
            AT_result = {
                "Success": True,
                "SAT": api_response.get('access_token', 'error'),
            }
        else:
            AT_result = {
                "Error": response.status_code,
                "Code": code,
                "Params": params,
                "Headers": headers,
                "Response": response.json(),
            }
    except Exception as e:
        AT_result = {
            "Error": "Post request to end-point /oauth/v2/accessToken failed",
            "Message": str(e),
            "Code": code,
            "Params": params,
            "Headers": headers,
        }

    SAT_result = {}
    accessToken = request.args.get('access_token', default='Not available', type=str)
    url = "https://api.linkedin.com/v2/salesAccessTokens?q=viewerAndDeveloperApp"
    headers = {
        "Authorization": "Bearer {}".format(accessToken),
        "X-Restli-Protocol-Version": "2.0.0"
    }
    SAT_response = requests.get(url, headers=headers)
    SAT_result = SAT_response.json()

    return render_template('SAT_retrieval.html', AccessTokenResponse=AT_result, SalesAccessTokenResponse=SAT_result)

if __name__ == '__main__':
    app.run(debug=True)
