# Assassin API for Assassin Android application
# CS m117, Winter 2017
# Team: Micah Cliffe, Christine Nguyen, Andrew Arifin, Nick Adair
# Primary maintainer: Micah Cliffe <micah.cliffe@ucla.edu>

from flask import Flask, json, render_template, request, Response

API_SECRET = "shh"
app        = Flask(__name__)

###########################################################################
''' Human user URLS '''

@app.route("/")
@app.route("/index")
@app.route("/index.htm")
@app.route("/index.html")
def index():
    return render_template('index.html')

###########################################################################
''' Android app URLs '''

@app.route("/api/stuff", methods=["POST"])
def stuff():
    return ""

###########################################################################
if __name__ == '__main__':
    app.debug = True
    app.run()
