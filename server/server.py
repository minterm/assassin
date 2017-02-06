# Assassin API for Assassin Android application
# CS m117, Winter 2017
# Team: Micah Cliffe, Christine Nguyen, Andrew Arifin, Nick Adair
# Primary maintainer: Micah Cliffe <micah.cliffe@ucla.edu>

from flask import Flask, json, render_template, request, Response

API_SECRET = "shh"
app        = Flask(__name__)

###########################################################################

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    template = "<!DOCTYPE html><html><body><h1>Assassin</h1><p>Server not implemented yet.</p></body></html>"
    #return render_template('index.html')
    return template

###########################################################################
if __name__ == '__main__':
    app.debug = True
    app.run()
