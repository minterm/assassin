#!/usr/bin/python
# -*- coding: utf-8 -*-

# Assassin API for Assassin Android application
# CS m117, Winter 2017
# Team: Micah Cliffe, Christine Nguyen, Andrew Arifin, Nick Adair
# Primary maintainer: Micah Cliffe <micah.cliffe@ucla.edu>

import random
from flask import Flask, jsonify, render_template, request, Response
import db_util as db

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

@app.route("/new", methods=["GET", "POST"])
def newGame():
    if request.method == "GET":
        return render_template('newGame.html')

    # else request.method == "POST"
    playerNames = []
    for form in request.form:
        playerNames.append(request.form[form])
    assassin_targets = _assignTargets(playerNames) 
    return jsonify(assassin_targets)
    #TODO: Create game number, create game table, etc 
    # get keys of dictionary with dictionaree.keys()
    return ""


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
@app.route("/api/info", methods=["GET"])
def info():
    g_id   = request.args.get("g_id")
    p_name = request.args.get("p_name")
    resp   = None
    if g_id is None or p_name is None:
        resp = Response("{}", status=400, mimetype='application/json')
    else:
        info = db.getInfo(g_id, p_name)
        resp = jsonify(info)
        if info is None:
            resp.status_code = 400
    return resp

###########################################################################
# GPS
@app.route("/api/gps", methods=["GET", "POST"])
def gps():
    if request.method == "GET":
        return getGPS(request)
    # else request.method == "POST"
    return postGPS(request)

def getGPS(req):
    # TODO
    # return GPS coordinates of target
    pass

def postGPS(req):
    # TODO
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
    # TODO
    # return status of player
    pass

def postStatus(req):
    # TODO
    # update player's status
    pass

###########################################################################
# Target
@app.route("/api/target", methods=["GET", "POST"])
def target():
    if request.method == "GET":
        return getTarget(request)
    # else request.method == "POST"
    return attackTarget(request)

def getTarget(req):
    # TODO
    # return target of player
    pass

def attackTarget(req):
    # TODO
    # kill a target
    # Does not update target directly
    pass

###########################################################################
''' Utility '''
###########################################################################

def _assignTargets(players):
    # accept a list of players
    # return a dictionary of {assassin: target}
    if len(players) <= 1:
        return None
    assassins = players # DON'T MODIFY ASSASSINS
    targets   = list(players)
    aT        = {}
    r         = random.SystemRandom()
    conflict  = True
    while conflict:
        conflict = False
        r.shuffle(targets)
        for assassin, target in zip(assassins, targets):
            if assassin == target:
                conflict = True
    for assassin, target in zip(assassins, targets):
        aT[assassin] = target
    return aT

def _chooseTarget(assassin, targets):
    print "Targets: " + str(targets)
    target = random.choice(targets)
    print "Target: " + target
    #TODO ERRRORORORORO
    if target == assassin:
        raw_input("target: " + target + ". assassin: " + assassin)
        if len(targets) is 1:
            raise Exception('One target left. Retry.')
        return _chooseTarget(assassin, targets)
    else:
        raw_input("target: " + target + ". assassin: " + assassin)
        return target

def _updateTarget():
    pass


###########################################################################
###########################################################################
if __name__ == '__main__':
    app.debug = True
    app.run()
