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
import hug
import requests
import json
from dataclasses import dataclass
# Helper function to perform queries
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
    sql = ("SELECT PassW FROM User WHERE Username='" + username +"';")
    query_password = query(sql, 'fetchone')
    if password == query_password[0]:
        return True



# Global Variable for authentication
authentication = hug.authentication.basic(auth)# Global Variable for authentication

# Helper function to get the userID from a username
def getUserID(username):
    userID = query("SELECT userID FROM User WHERE username='" + username + "';", 'fetchone')
    if(userID):
        return userID
    else:
        return

# Helper function to get the postID of a post
def getPostID(postID):
    post = query("SELECT postID FROM Post WHERE postID='" + str(postID) + "';", 'fetchone')
    return post

# Helper function to check whether a post is a repost
def isRepost(content):
    postID = query("SELECT postID FROM Post Where content='" + content + "'", 'fetchone') 
    if(postID):
        print('This is a repost...')
        return postID
    else:
        print('Not a repost...')
        return postID
    
# Routes ---------------------------------------------------------------

# Home screen
@hug.get("/")   
def home():
    return 'CPSC 449 Microblog API - A prototype API for a microblog service.'

# Get a post
@hug.get("/getPost", relationship="postID=value")
def getPost(postID):
    print(postID)
    post = query("SELECT * FROM Post WHERE postID='" + postID + "';", 'fetchone')
    return post

# Get all users
@hug.get("/getUsers")
def getUsers():
    all_users = query("SELECT * FROM User;", 'fetchall')
    return all_users

# Create a Post
@hug.post("/post", requires=authentication)
def post(userID, orgPostID, link, content):
        print('Calling Post Endpoint...')
        postData={
            "userID": userID,
            "orgPostID": 0,
            "link": 'N/A',
            "content": content 
        }
        postID = isRepost(postData["content"])
        if(postID):
            orgPostID = postID
            postData["orgPostID"] = postID[0]
            link = 'localhost:5000/getPost?postID=' + str(getPostID(postID[0])[0])
            postData["link"] = 'localhost:5000/getPost?postID=' + str(getPostID(postID[0])[0])
            sql = ('INSERT INTO Post (userID, orgPostID, link, content, timestamp) VALUES (%i, %i,\'%s\',\'%s\',%s);' % (userID, orgPostID[0], link, str(content), "datetime('now')"))
        else:
            print('keeping default postData')
            sql = ('INSERT INTO Post (userID, orgPostID, link, content, timestamp) VALUES (%i, %i,\'%s\',\'%s\',%s);' % (userID, 0, postData['link'], str(content), "datetime('now')"))  
        post = query(sql, 'fetchone')
        return {"new_post": postData}

# Follow a User
@hug.post("/follow", relationship='username=value&followName=value', requires=authentication)
def follow(username:hug.types.text, followName:hug.types.text):
    #First get the id's of both usernames s
    userID = getUserID(username)
    followID = getUserID(followName)

    print('UserID:',userID[0], 'followID:', followID[0])
    followRelationshipData = {
        "userID": userID,
        "followID": followID
    }
    followRelationship = query('INSERT INTO Following (influencerID, followerID) VALUES(%i,%i);' %(followID[0], userID[0]), 'fetchone')
    return {"new_followRelationship": followRelationshipData}

# Create a user
@hug.post("/register")
def create_user(username, passW, email, bio):
    print('Calling register endpoint...')

    userData={
        "username": username,
        "psssW": passW,
        "email": email,
        "bio": bio
    }

    sql = 'INSERT INTO User(username,passW,email,bio) VALUES(\'%s\',\'%s\',\'%s\',\'%s\');' % (username, passW, email, bio )    
    userData = query(sql, 'fetchone')
    return {"username": username, 
            "passW": passW,
            "email": email,
            "bio": bio}
