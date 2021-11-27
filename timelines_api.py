# CPSC 449 - Project 2: Microblog Service
#
# Names:
# Chaney Chantipaporn
# Nhat Nguyen
# Tony Nguyen
#
# Emails:
# Chaney.chanti@csu.fullerton.edu
# Nhatmn2@csu.fullerton.edu
# Tonyxd14@csu.fullerton.edu
#

import string
import textwrap
import logging
import sqlite3
from dataclasses import dataclass
import hug
import requests
import json


# For query use
def query(sqlStatement, fetch):
    print('RUNNING SQL: ', sqlStatement + '\n')
    conn = sqlite3.connect('microblog.db') 
    c = conn.cursor()
    c.execute(sqlStatement)
    if fetch == 'fetchone':
        result = c.fetchone()
    elif fetch == 'fetchall':
        result = c.fetchall()
    conn.commit()
    conn.close()
    return result

# Function to authenticate a user
def auth(username, password):
    #query database to compare username and password to see if theres a matching tuple
    sql = ("SELECT PassW FROM User WHERE Username='" + username +"'")
    query_password = query(sql, 'fetchone')
    if password == query_password[0]:
        return True
    else:
        print('Failed to authenticate user...')

# Global variable used for authentication
authentication = hug.authentication.basic(auth)

 # Function to get a user's ID
def getUserID(username):
    userID = query("SELECT userID FROM User WHERE username='" + username + "';", 'fetchone')
    if(userID):
        return userID

# Routes ---------------------------------------------------------------

# Home screen
@hug.get("/")   
def home():
    return 'CPSC 449 Microblog API - A prototype API for a timelines.'

# User Timeline - Get all posts from a user
@hug.get("/user/timeline", relationship='username=value', requires=authentication)
def getUsers(username:hug.types.text):
    userID = getUserID(username)
    user_timeline = query("SELECT * FROM Post WHERE userID=" + str(userID[0]) + ";", 'fetchall')
    return user_timeline

# Home Timeline - Get all posts from who the user follos, must be authenticated
@hug.get("/home/timeline",relationship='username=value', requires=authentication)
def getUsers(username):
    userID = getUserID(username)
    home_timeline = query("SELECT * FROM Post where userID =(SELECT influencerID FROM Following WHERE followerID=" + str(userID[0]) + ");", 'fetchall')
    return home_timeline

# Public Timeline - Get all posts form all users
@hug.get("/public/timeline")
def getUsers():
    public_timeline = query("SELECT * FROM Post;", 'fetchall'), 
    return public_timeline
