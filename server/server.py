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
    # TODO: use template instead of just returning text
    if request.method == "GET":
        return render_template('newGame.html')
    # else request.method == "POST"
    playerNames = []
    for form in request.form:
        playerNames.append(request.form[form])
    assassin_targets = _assignTargets(playerNames)
    g_id = _createGameID()
    if not g_id: return "Too many games currently running."
    db.createGameTable(g_id)
    for assassin in assassin_targets:
        if not db.addPlayer(g_id, assassin):
            db.deleteGameTable(g_id)
            return "Failed to add assassin: " + assassin
        if not db.setTarget(g_id, assassin, assassin_targets[assassin]):
            db.deleteGameTable(g_id)
            return "Failed to add target: " + assassin_targets[assassin]
    return "Open the mobile app and join game: " + g_id


@app.route("/view")
def viewGame():
    g_id = request.args.get("g_id")
    if g_id is None:
        return render_template('viewGameSetup.html')
    # Get info from database and display on page for given g_id
    ''' if g_id is real, then render viewGame. else, return invalid '''
    g_id = db.tableName(g_id)
    if g_id not in db.getGameIDs():
        return render_template('invalidGame.html')
    info = _formatView(db.getView(g_id))
    return render_template('viewGame.html', g_id=g_id, info=info)

def _formatView(view):
    form = []
    for v in view:
        p_id   = str(v["p_id"])
        p_name = str(v["p_name"])
        if (v["p_id"]):
            alive = "alive"
        else:
            alive = "dead"
        form.append(p_id + " | " + p_name + " | " + alive)
    return form

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
# Join Game
@app.route("/api/join", methods=["POST"])
def join():
    # provide assassin's MAC address and location
    try:
        data   = request.get_json(force=True)
        p_name = data["p_name"]
        g_id   = data["g_id"]
        mac    = data["mac"]
        loc    = data["loc"]
    except Exception as e:
        print e
        resp             = jsonify({"success": "false", "error": e})
        resp.status_code = 400
        return resp
    error = False
    if (not db.setMAC(g_id, p_name, mac)): error = True
    if (not db.setLocation(g_id, p_name, loc)): error = True
    if error:
        resp             = jsonify({"success": "false"})
        resp.status_code = 400
        return resp
    return jsonify({"success": "true"})

###########################################################################
# Post Location
@app.route("/api/gps", methods=["POST"])
def gps():
    # update assassin's location
    try:
        data   = request.get_json(force=True)
        p_name = data["p_name"]
        g_id   = data["g_id"]
        loc    = data["loc"]
    except Exception as e:
        print e
        resp             = jsonify({"success": "false", "error": e})
        resp.status_code = 400
        return resp
    if (db.setLocation(g_id, p_name, loc)): 
        return jsonify({"success": "true"})
    resp             = jsonify({"success": "false"})
    resp.status_code = 400
    return resp

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

def _createGameID():
    ids = db.getGameIDs()
    if len(ids) > 999:
        # Too many games
        return False
    g_id = "g_" + str(random.randint(0,999))
    while (g_id in ids):
        g_id = "g_" + str(random.randint(0,999))
    return g_id

###########################################################################
###########################################################################
if __name__ == '__main__':
    app.debug = True
    app.run()
