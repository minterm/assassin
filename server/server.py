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

@app.route("/instructions")
def instructions():
    return render_template('instructions.html')

@app.route("/new", methods=["GET", "POST"])
def newGame():
    if request.method == "GET":
        return render_template('newGame.html')
    # else request.method == "POST"
    playerNames = []
    for form in request.form:
        playerNames.append(request.form[form])
    assassin_targets = _assignTargets(playerNames)
    g_id = _createGameID()
    if not g_id:
        err = "Too many games currently running."
        return render_template('gameCreated.html', g_id=g_id,
                                success=False, error=err)
    db.createGameTable(g_id)
    for assassin in assassin_targets:
        if not db.addPlayer(g_id, assassin):
            db.deleteGameTable(g_id)
            err = "Failed to add assassin: " + assassin
            return render_template('gameCreated.html', g_id=g_id, 
                                    success=False, error=err)
        if not db.setTarget(g_id, assassin, assassin_targets[assassin]):
            db.deleteGameTable(g_id)
            err = "Failed to add target: " + assassin_targets[assassin]
            return render_template('gameCreated.html', g_id=g_id, 
                                    success=False, error=err)
    return render_template('gameCreated.html', g_id=g_id, success=True, 
                            error="")


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

###########################################################################
''' Android app URLs '''
###########################################################################
# GetInfo
@app.route("/api/info", methods=["GET"])
def info():
    # Takes parameters: g_id, p_name
    # Return p_id, alive, t_loc, t_name, t_mac, p_name, g_id
    g_id   = request.args.get("g_id")
    p_name = request.args.get("p_name")
    resp   = None

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
# Get Game Status
@app.route("/api/gameplay", methods=["GET"])
def gameplay():
    # Takes parameters: g_id
    # Return if game is 0 (waiting), 1 (active), 2 (finished) with winner
    g_id  = request.args.get("g_id")
    gp    = db.getActive(g_id)
    ret   = {}
    gSize = len(gp)
    if gSize == 1:
        ret = {"status": 2, "winner": gp[0]}
    else:
        macLen = len(db.getMacNumber(g_id))
        actLen = len(gp)
        if macLen < actLen:
            ret = {"status": 0}
        else:
            ret = {"status": 1}
    return jsonify(ret)

###########################################################################
# Join Game
@app.route("/api/join", methods=["POST"])
def join():
    # provide assassin's MAC address and location
    # Takes data: p_name, g_id, mac, loc
    # Return {"success": "true"/"false" [,"error": e]}
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
    # Takes data: p_name, g_id, loc
    # Return {"success": "true"/"false" [,"error": e]}
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
    # kill a target
    # Does not update target directly
    # Takes data: p_name, g_id, target = mac of target
    # Return {"success": "false" [,"error": e]}
    # Return {"success": "true", "target": newTarget]}
    try:
        data   = request.get_json(force=True)
        p_name = data["p_name"]
        g_id   = data["g_id"]
        target = data["target"]
    except Exception as e:
        print e
        resp             = jsonify({"success": "false", "error": e})
        resp.status_code = 400
        return resp
    arg = db.getStatus(g_id,target)
    if int(db.getStatus(g_id, target)) == 0:
        resp = jsonify({"success": "false", "error":
                        "target already dead"})
        resp.status_code = 400
        return resp
    if (db.setStatus(g_id, target, 0)): 
        newTarget = _updateTarget(g_id, p_name, target)
        resp = {"success": "true", "target": newTarget}
        return jsonify(resp)
    resp             = jsonify({"success": "false"})
    resp.status_code = 400
    return resp

###########################################################################
''' Utility '''
###########################################################################

def _assignTargets(players):
    # accept a list of players
    # return a dictionary of {assassin: target}
    if len(players) <= 1:
        return None
    assassins = list(players)
    r         = random.SystemRandom()
    r.shuffle(assassins)
    aT        = {}
    n         = len(assassins) - 1
    for i in range(0, n):
        aT[assassins[i]] = assassins[i+1]
    aT[assassins[n]] = assassins[0]
    return aT


def _updateTarget(g_id, p_name, target):
    newTarget = db.getTarget(g_id, target)
    db.setTarget(g_id, p_name, newTarget)
    return newTarget

def _createGameID():
    ids = db.getGameIDs()
    if ids and len(ids) > 999:
        # Too many games
        return False
    g_id = "g_" + str(random.randint(0,999))
    while (ids and g_id in ids):
        g_id = "g_" + str(random.randint(0,999))
    return g_id

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
###########################################################################
if __name__ == '__main__':
    app.debug = True
    app.run()
