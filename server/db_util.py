#!/usr/bin/python
# -*- coding: utf-8 -*-

# DB util for Assassin Android application
# CS m117, Winter 2017
# Team: Micah Cliffe, Christine Nguyen, Andrew Arifin, Nick Adair
# Primary maintainer: Micah Cliffe <micah.cliffe@ucla.edu>

import MySQLdb as mdb
import sys

HOST     = 'localhost'
USERNAME = 'assassin'
PASSWORD = 'assassin'
DATABASE = 'Assassin'

###############################################################################
''' Setters '''

def createGameTable(g_id):
    # g_id = game ID = table name
    table_name = tableName(g_id)
    col1 = "p_id INT NOT NULL AUTO_INCREMENT"
    col2 = "p_name VARCHAR(45) DEFAULT NULL"
    col3 = "alive INT(1) DEFAULT 1"
    col4 = "location TEXT DEFAULT NULL"
    col5 = "target VARCHAR(45) DEFAULT NULL"
    prim = "PRIMARY KEY(p_id)"
    cmd  = "CREATE TABLE IF NOT EXISTS " + table_name + "("
    cmd += col1 + ", " + col2 + ", " + col3 + ", " + col4 + ", " + col5 + ", "
    cmd += prim + ") engine=InnoDB"
    # TODO: change primary key to p_name maybe
    if (_execute(cmd)):
        print table_name + " was created."
        return True
    print "Unable to create " + table_name + "."
    return False

def addPlayer(g_id, p_name):
    if len(p_name) > 45:
        print "Player name too long."
        return False
    t_name = tableName(g_id)
    if not _checkUnique(t_name, p_name):
        print "Player name not unique."
        return False
    cmd = "INSERT INTO " + t_name + "(p_name) VALUES('" + p_name + "')"
    if (_execute(cmd)):
        print p_name + " was added to " + t_name + "."
        return True
    print "Unable to add " + p_name + " to " + t_name + "."
    return False

def _checkUnique(t_name, p_name):
    resp = _query("SELECT p_name FROM " + t_name)
    for p in resp:
        if p[0] == p_name:
            return False
    return True

def setLocation(g_id, p_name, loc):
    t_name = tableName(g_id)
    cmd  = "UPDATE " + t_name + " SET location = '" + loc + "' WHERE "
    cmd += "p_name = '" + p_name + "'"
    if (_execute(cmd)):
        print p_name + " location is now " + loc + "."
        return True
    print "Unable to update " + p_name + " location."
    return False

def setTarget(g_id, p_name, target):
    # TODO: Check if target is another player in the game
    if len(target) > 45:
        print "Target name too long."
        return False
    t_name = tableName(g_id)
    cmd  = "UPDATE " + t_name + " SET target = '" + target + "' WHERE "
    cmd += "p_name = '" + p_name + "'"
    if (_execute(cmd)):
        print p_name + " target is now " + target + "."
        return True
    print "Unable to update " + p_name + " target."
    return False

def deleteGameTable(g_id):
    t_name = tableName(g_id)
    cmd    = "DROP TABLE IF EXISTS " + t_name
    if (_execute(cmd)):
        print t_name + " was dropped."
        return True
    print "Unable to drop " + t_name + "."
    return False

###############################################################################
''' Getters '''

def getTables():
    return(_query("SHOW TABLES"))

def getLocation(g_id, p_name):
    t_name = tableName(g_id)
    resp = _query("SELECT location FROM " + t_name + " WHERE p_name='" + 
                   p_name + "'")
    if resp:
        return resp[0][0]
    return resp

def getTarget(g_id, p_name):
    t_name = tableName(g_id)
    resp = _query("SELECT target FROM " + t_name + " WHERE p_name='" + 
                   p_name + "'")
    if resp:
        return resp[0][0]
    return resp

def getStatus(g_id, p_name):
    t_name = tableName(g_id)
    resp = _query("SELECT alive FROM " + t_name + " WHERE p_name='" + 
                   p_name + "'")
    if resp:
        return resp[0][0]
    return resp

def getInfo(g_id, p_name):
    # returns dictionary of info
    t_name = tableName(g_id)
    resp   = _query("SELECT p_id, alive, location, target FROM " + t_name + 
                    " WHERE p_name='" + p_name + "'")
    if resp:
        resp = resp[0]
        d = {"p_id": resp[0], "alive": resp[1], "location": resp[2],
             "target": resp[3], "p_name": p_name, "g_id": t_name} 
        return d
    return None

###############################################################################
''' functions for the db_util module only '''

def _query(query, args=()):
    rv  = None
    con = None
    try:
        con = mdb.connect(HOST, USERNAME, PASSWORD, DATABASE);
        cur = con.cursor()
        cur.execute(query, args)
        rv  = cur.fetchall()
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:    
        if con:    
            con.close()
    return rv

def _execute(command, args=()):
    completed = False
    try:
        con = mdb.connect(HOST, USERNAME, PASSWORD, DATABASE);
        con.cursor().execute(command, args)
        con.commit()
        completed = True
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:    
        if con:    
            con.close()
    return completed

def tableName(g_id):
    # Accepts g_id as an integer, string, or tableName()
    if type(g_id) is str or type(g_id) is unicode:
        if len(g_id) > 2:
            if g_id[0:2] == "g_":
                return g_id
    return "g_" + str(g_id)

###############################################################################
if __name__ == "__main__":
    print _query("SELECT VERSION()")

    #deleteGameTable(123)
    #createGameTable(123)
    addPlayer(123, "swag 2")
    setLocation(123, "swag 2", "right there dude")
    setTarget("123", "swag", "swag 2")
    setTarget("123", "swag 2", "swag")
    print getInfo("g_123", "swag")
    #deleteGameTable(123)

    for resp in getTables():
        print resp[0]