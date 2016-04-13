from flask import Flask, render_template
from flask import request
import json
import Correlation

app = Flask(__name__)


@app.route("/Home")
def template_test():
    return render_template('Home.html',)


@app.route("/$AAPL")
def Apps():
    return render_template('Apple.html')


@app.route("/$AAPL_FA")
def Apple_FA():
    return render_template('Apple_FA.html')


@app.route("/$GOOG")
def Google():
    return render_template('Google.html')


@app.route("/$FB")
def Facebook():
    decide = Correlation.correlation()
    return render_template('FB.html', decision=decide)

@app.route("/$FB_FA")
def FB_FA():
    return render_template('FB_FA.html')

@app.route("/$GLEN")
def GLEN():
    return render_template('GLEN.html')

@app.route("/$ITV")
def ITV():
    return render_template('ITV.html')


if __name__ == '__main__':
    app.run(debug = True)
