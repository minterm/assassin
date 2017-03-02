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
ID_TABLE = 'ID_Table'

#TODO: Constantly have table of open game ids

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
    col6 = "p_mac VARCHAR(17) DEFAULT NULL"
    col7 = "t_mac VARCHAR(17) DEFAULT NULL"
    prim = "PRIMARY KEY(p_id)"
    cmd  = "CREATE TABLE IF NOT EXISTS " + table_name + "("
    cmd += col1 + ", " + col2 + ", " + col3 + ", " + col4 + ", " + col5 + ", "
    cmd += col6 + ", " + col7 + ", "
    cmd += prim + ") engine=InnoDB"
    # TODO: change primary key to p_name maybe
    #TODO: Add getters and setters for MAC addresses
    if (_execute(cmd)):
        print table_name + " was created."
        _addGameID(table_name)
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
        print p_name + "'s target is now " + target + "."
        return True
    print "Unable to update " + p_name + " target."
    return False

def setMAC(g_id, p_name, mac):
    if len(mac) > 17:
        print "Invalid MAC address."
        return False
    t_name = tableName(g_id)
    cmd  = "UPDATE " + t_name + " SET p_mac = '" + mac + "' WHERE "
    cmd += "p_name = '" + p_name + "'"
    if (_execute(cmd)):
        print p_name + "'s MAC is now " + mac + "."
        return True
    print "Unable to update " + p_name + " MAC."
    return False

def setTargetMAC(g_id, p_name, t_mac):
    if len(t_mac) > 17:
        print "Invalid target MAC address."
        return False
    t_name = tableName(g_id)
    cmd  = "UPDATE " + t_name + " SET t_mac = '" + t_mac + "' WHERE "
    cmd += "p_name = '" + p_name + "'"
    if (_execute(cmd)):
        print p_name + "'s target MAC is now " + t_mac + "."
        return True
    print "Unable to update " + p_name + " target MAC."
    return False

def deleteGameTable(g_id):
    t_name = tableName(g_id)
    cmd    = "DROP TABLE IF EXISTS " + t_name
    if (_execute(cmd)):
        print t_name + " was dropped."
        _removeGameID(t_name)
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

def getGameIDs():
    resp = _query("SELECT g_id FROM " + ID_TABLE)
    if resp:
        ids = []
        for r in resp:
            ids.append(r[0])
        return tuple(ids)
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
# ID table functions

def createIdTable():
    col1 = "p_id INT NOT NULL AUTO_INCREMENT"
    col2 = "g_id TEXT DEFAULT NULL"
    prim = "PRIMARY KEY(p_id)"
    cmd  = "CREATE TABLE IF NOT EXISTS " + ID_TABLE + "("
    cmd += col1 + ", " + col2 + ", "
    cmd += prim + ") engine=InnoDB"
    if (_execute(cmd)):
        print ID_TABLE + " was created."
        return True
    print "Unable to create " + ID_TABLE + "."
    return False

def _addGameID(g_id):
    if (type(g_id) == int and g_id > 999) or (type(g_id) == str and len(g_id) > 5):
        print "g_id too large."
        return False
    t_name = ID_TABLE
    r_name = tableName(g_id)
    cmd = "INSERT INTO " + t_name + "(g_id) VALUES('" + r_name + "')"
    if (_execute(cmd)):
        print r_name + " was added to " + t_name + "."
        return True
    print "Unable to add " + r_name + " to " + t_name + "."
    return False

def _removeGameID(g_id):
    r_name = tableName(g_id)
    cmd    = "DELETE FROM " + ID_TABLE + " WHERE g_id='" + r_name + "'" 
    if (_execute(cmd)):
        print r_name + " was deleted."
        return True
    print "Unable to delete " + r_name + "."
    return False

###############################################################################
if __name__ == "__main__":
    print _query("SELECT VERSION()")

    '''

    #deleteGameTable(123)
    #createGameTable(123)
    addPlayer(123, "swag 2")
    setLocation(123, "swag 2", "right there dude")
    setTarget("123", "swag", "swag 2")
    setTarget("123", "swag 2", "swag")
    print getInfo("g_123", "swag")
    #deleteGameTable(123)
    '''
    '''
    createIdTable()
    _addGameID(666)
    _removeGameID(666)
    '''
    print getGameIDs()

    for resp in getTables():
        print resp[0]
