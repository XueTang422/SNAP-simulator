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
                    + secret_vars['client_id'] + "&redirect_uri=http://ltx1-app2411.stg.linkedin.com:13072/OAuth/return_oauth&state="
                    + secret_vars['state_secret'] + "&scope=r_sales_nav_display")


@app.route('/OAuth/return_oauth', methods=['GET', 'POST'])
def return_oauth():
    SAT_result = {}
    code = request.args.get('code', default='Not available', type=str)
    params = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': secret_vars['client_id'],
        'client_secret': secret_vars['client_secret'],
        'scope': 'r_sales_nav_display',
        'redirect_uri': 'http://ltx1-app2411.stg.linkedin.com:13072/OAuth/return_oauth',
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    try:
        response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            api_response = response.json()
            SAT_result = {
                "Success": True,
                "SAT": api_response.get('access_token', 'error'),
            }
        else:
            SAT_result = {
                "Error": response.status_code,
                "Code": code,
                "Params": params,
                "Headers": headers,
                "Response": response.json(),
            }
    except Exception as e:
        SAT_result = {
            "Error": "Post request to end-point /oauth/v2/accessToken failed",
            "Message": str(e),
            "Code": code,
            "Params": params,
            "Headers": headers,
        }

    return render_template('SAT_retrieval.html', SalesAccessTokenResponse=SAT_result)

if __name__ == '__main__':
    app.run(debug=True)
