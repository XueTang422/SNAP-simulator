from flask import Flask, render_template
from routes import oauth_routes

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('snap_display_widget_playground.html')

if __name__ == '__main__':
    app.run(debug=True)
