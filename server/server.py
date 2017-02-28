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

    # test behavior without database
    resp = {}
    resp['alive'] = 1
    resp['g_id']  = g_id
    resp['location'] = "right here"
    resp['p_id'] = 1
    resp['p_name'] = p_name
    resp['target'] = p_name + "'s target"
    return jsonify(resp)

    # actual behavior
    if g_id is None or p_name is None:
        resp = Response("{}", status=400, mimetype='application/json')
    else:
        info = db.getInfo(g_id, p_name)
        resp = jsonify(info)
        if info is None:
            resp.status_code = 400
    return resp

###########################################################################
# Post Location
@app.route("/api/gps", methods=["POST"])
def gps():
    # TODO
    # update assassin's location
    return ""

###########################################################################
# Attack Target
@app.route("/api/attack", methods=["POST"])
def attackTarget():
    # TODO
    # kill a target
    # Does not update target directly
    return ""

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

def _updateTarget():
    pass

###########################################################################
###########################################################################
if __name__ == '__main__':
    app.debug = True
    app.run()
