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

#TODO: Primary key username instead of p_id maybe

###############################################################################
''' Submit Info '''

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
    if (execute(cmd)):
        print table_name + " was created."
        return True
    print "Unable to create " + table_name + "."
    return False

def addPlayerToGame(g_id, p_name):
    t_name = tableName(g_id)
    cmd = "INSERT INTO " + t_name + "(p_name) VALUES('" + p_name + "')"
    if (execute(cmd)):
        print p_name + " was added to " + t_name + "."
        return True
    print "Unable to add " + p_name + " to " + t_name + "."
    return False

def updateLocation(g_id, p_name, loc):
    t_name = tableName(g_id)
    cmd  = "UPDATE " + t_name + " SET location = '" + loc + "' WHERE "
    cmd += "p_name = '" + p_name + "'"
    if (execute(cmd)):
        print p_name + " location is now " + loc + "."
        return True
    print "Unable to update " + p_name + " location."
    return False

def updateTarget(g_id, p_name, target):
    pass

def deleteGameTable(g_id):
    t_name = tableName(g_id_
    cmd    = "DROP TABLE IF EXISTS " + t_name
    if (execute(cmd)):
        print t_name + " was dropped."
        return True
    print "Unable to drop " + t_name"."
    return False

###############################################################################
''' Retrieve Info '''

def getPlayerLocation(g_id, p_name):
    pass

def getTarget(g_id, p_name):
    pass

def getStatus(g_id, p_name):
    pass

def getInfo(g_id, p_name):
    pass #THIS ONE IS THE MOST IMPORTANT

###############################################################################
def query(query, args=()):
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

def execute(command, args=()):
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
    return "g_" + str(g_id)

###############################################################################
if __name__ == "__main__":
    print query("SELECT VERSION()")
    print query("SHOW TABLES")

    createGameTable(123)
    addPlayerToGame(123, "swag")
    deleteGameTable(123)

    print query("SHOW TABLES")
