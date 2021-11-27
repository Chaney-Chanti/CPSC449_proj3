# CPSC 449 - Project 2: Microblog Service
#
# Names:
# Chaney Chantipaporn
# Nhat Nguyen
# Tony Nguyen
#
# Emails:
# Chaney.chanti@csu.fullerton.edufullerton.edu
# Nhatmn2@csu.fullerton.edu
# Tonyxd14@csu.fullerton.edu
###############################################

import sqlite3


# Open connection
conn = sqlite3.connect('microblog.db') 
c = conn.cursor()

# Create a User Table
c.execute("""CREATE TABLE IF NOT EXISTS User(
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            passW TEXT,
            email TEXT,
            bio TEXT
        )""")

# Create a Posts Table
#if originalpost is 0, its not a repost
c.execute("""CREATE TABLE IF NOT EXISTS Post(
            postID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER,
            orgPostID INTEGER, 
            link TEXT,
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY(userID) REFERENCES user(userID),
            FOREIGN KEY(orgPostID) REFERENCES Post(postId)
    )""")

# Creates a following table
#followerID follows the influenceID
c.execute("""CREATE TABLE IF NOT EXISTS Following(
            influencerID INTEGER,
            followerID INTEGER,
            FOREIGN KEY(influencerID) REFERENCES user(userID),
            FOREIGN KEY(followerID) REFERENCES user(userID)
    )""")

# Inputs data for Users
c.execute("INSERT INTO User VALUES('1','Chaney','chaneypassword','chaney.chantipaporn@gmail.com','chaneybio')")
c.execute("INSERT INTO User VALUES('2','Nhat','nhatpassword','nhat.nguyen@gmail.com','nhatbio')")
c.execute("INSERT INTO User VALUES('3','Tony','tonypassword','tony.tony@gmail.com','tonybio')")
c.execute("INSERT INTO User VALUES('4','Someone','someonepassword','someone.else@gmail.com','someonebio')")

# Inputs data for posts
c.execute("INSERT INTO Post VALUES('1','1', '0','N/A','chaneypost', datetime('now'))")
c.execute("INSERT INTO Post VALUES('2','2', '0','N/A','nhatpost', datetime('now'))")
c.execute("INSERT INTO Post VALUES('3','3', '0','N/A','tonypost', datetime('now'))")
c.execute("INSERT INTO Post VALUES('4','3', '0','N/A','hi hello', datetime('now'))")
c.execute("INSERT INTO Post VALUES('5','3', '0','N/A','goodbye', datetime('now'))")
c.execute("INSERT INTO Post VALUES('6','3', '0','N/A','i love to eat', datetime('now'))")
c.execute("INSERT INTO Post VALUES('7','1', '0','N/A','im too busy!', datetime('now'))")
c.execute("INSERT INTO Post VALUES('8','1', '0','N/A','i want to play tennis', datetime('now'))")
c.execute("INSERT INTO Post VALUES('9','1', '0','N/A','sorry playing valorant', datetime('now'))")
c.execute("INSERT INTO Post VALUES('10','2', '0','N/A','i live on the east coast', datetime('now'))")
c.execute("INSERT INTO Post VALUES('11','2', '0','N/A','i applied to amazon', datetime('now'))")
c.execute("INSERT INTO Post VALUES('12','2', '0','N/A','my last name is nguyen', datetime('now'))")

# Inputs data for Followingc.execute("INSERT INTO Following VALUES('1','3')") 
c.execute("INSERT INTO Following VALUES('1','4')")
c.execute("INSERT INTO Following VALUES('2','3')")
c.execute("INSERT INTO Following VALUES('3','2')")

conn.commit()

# Close connection
conn.close()
