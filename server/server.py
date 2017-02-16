# Assassin API for Assassin Android application
# CS m117, Winter 2017
# Team: Micah Cliffe, Christine Nguyen, Andrew Arifin, Nick Adair
# Primary maintainer: Micah Cliffe <micah.cliffe@ucla.edu>

from flask import Flask, json, render_template, request, Response

API_SECRET = "shh"
app        = Flask(__name__)

###########################################################################
''' Human user URLS '''
###########################################################################

@app.route("/")
@app.route("/index")
@app.route("/index.htm")
@app.route("/index.html")
def index():
    return render_template('index.html')

@app.route("/new")
def newGame():
    return render_template('newGame.html')

@app.route("/view")
def viewGame():
    g_id = request.args.get("g_id")
    if g_id is None:
        return render_template('viewGameSetup.html')
    # Get info from database and display on page for given g_id
    return g_id
    return render_template('viewGame.html', g_id=g_id)

###########################################################################
''' Android app URLs '''
###########################################################################

# GetInfo
@app.route("/api/info/<player>", methods=["GET"])
def info(player):
    # return info for player by checking database
    pass

###########################################################################
# GPS
@app.route("/api/gps", methods=["GET", "POST"])
def gps():
    if request.method == "GET":
        return getGPS(request)
    # else request.method == "POST"
    return postGPS(request)

def getGPS(req):
    # return GPS coordinates of target
    pass

def postGPS(req):
    # update assassin's location
    pass

###########################################################################
# Status
@app.route("/api/status", methods=["GET", "POST"])
def status():
    if request.method == "GET":
        return getStatus(request)
    # else request.method == "POST"
    return postStatus(request)

def getStatus(req):
    # return status of player
    pass

def postStatus(req):
    # update player's status
    pass

###########################################################################
###########################################################################
if __name__ == '__main__':
    app.debug = True
    app.run()
