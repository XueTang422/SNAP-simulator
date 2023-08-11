import requests
from flask import redirect, render_template, url_for
from secrets import secret_vars

def begin_oauth():
    return redirect("https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id="
                    + secret_vars['client_id'] + "&redirect_uri=" + url_for('return_oauth', _external=True)
                    + "&state=" + secret_vars['state_secret'] + "&scope=r_sales_nav_display")

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
                "accessToken": api_response.get('access_token', 'error'),
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
    accessToken = AT_result.get('accessToken', 'error')
    url = "https://api.linkedin.com/v2/salesAccessTokens?q=viewerAndDeveloperApp"
    headers = {
        "Authorization": "Bearer {}".format(accessToken),
        "X-Restli-Protocol-Version": "2.0.0"
    }
    SAT_response = requests.get(url, headers=headers)
    SAT_result = SAT_response.json()

    return render_template('SAT_retrieval.html', AccessTokenResponse=AT_result, SalesAccessTokenResponse=SAT_result)
