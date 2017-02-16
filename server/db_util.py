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
        con.cursor().execute(query, args)
        con.commit()
        completed = True
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
    finally:    
        if con:    
            con.close()
    return completed

###############################################################################
if __name__ == "__main__":
    print query("SELECT VERSION()")
    print query("SHOW TABLES")
    table_name = "exampleGame"
    col1 = "p_id INT(11) NOT NULL AUTOINCREMENT"
    col2 = "p_name VARCHAR(45) DEFAULT NULL"
    col3 = "alive INT(1) DEFAULT 1"
    col4 = "location TEXT DEFAULT NULL"
    prim = "PRIMARY KEY(p_id)"
    cmd  = "CREATE TABLE IF NOT EXISTS " + table_name + "("
    cmd += col1 + ", " + col2 + ", " + col3 + ", " + col4 + ", "
    cmd += prim + ") engine=InnoDB"
    print execute(cmd)
    print query("SHOW TABLES")
