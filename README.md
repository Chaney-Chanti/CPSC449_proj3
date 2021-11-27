# CPSC 449 - Project 2: Micrblogging Service

## Group Members:

Chaney Chantipaporn

Nhat Nguyen

Tony Nguyen

## Project Requirements
This project will run using Tuffix 2020 using Python 3.8.10 and will be implemented using Hug, sqlite_tils, and Request libraries. 
An installation of ruby-foreman, httpie, sqlite3, sqlite-utils, hug, and gunicorn may be required. 

## Project Description

In this project we are creating two RESTful microservices. One for users, and one for timelines. 

## How to Run the Program

The following steps are required to prepare to run the project.
1. Install the pip package installer and other tools by running the following commands:
    sudo apt update
    sudo apt install --yes python3-pip ruby-foreman httpie sqlite3

2. Install the Hug and sqlite-utils libraries by running the following command:
    python3 -m pip install hug sqlite-utils

3. Log out then back in to pick up changes to your PATH before trying to run the hug or sqlite-utils commands.
Install the HAProxy and Gunicorn servers by running the following commands:
    sudo apt install --yes haproxy gunicorn

4. Once everything has installed, locate the project folder in the terminal. Use the cd command to the project folder.

5. Then run the command:
    ### To initialize the database, type:
        python3 sqlite.py
    ### To start the gunicorn servers, type:
        foreman start
    
6. The application will run on six different ports (5000, 5100, 5200, 5300, 5400, 5500). The application can be tested using HTTPie. 

7. Example CURL/HTTPIE Commands to run:
    ### User_API:

        localhost:5000/getUsers
        
        localhost:5000/getPost?postID=3

        http -a Tony:tonypassword GET localhost:5000/post {"userID": 3, "orgPostID": 0, "link": "N/A", "content": "awesome content!"}

        localhost:5000/follow?username=Chaney&followName=Tony

        localhost:5000/register    
        curl -X POST localhost:5000/register -H'Content-Type:application/json' -d '{"username":"jeff","passW":"jeffpassword","email":"jeff.hwang@gmail.com","bio":"jeffbio"}'

    ### Timelines_API:
        *All timeline API utilizes query parameters*
        localhost:5100/user/timeline?username=Chaney
        localhost:5100/home/timeline?username=Chaney
        localhost:5100/public/timeline
 
8. Configure 3 timeline services and 1 user service. 

9. Add the new like service using Redis 

    * /like 
        - POST method take in the username and the postname (postID)
        - have a counter to increase the number of likes in a particular post 
         
    * /getPostLikes  
        - GET method take in the postname (postID)
        - return the number of like a post have  
    
    * /getUserLikes 
        - GET method return all the postnames (postIDs) that a specific user has liked 
    
    * /getPopularPosts
        - GET method return the 5 most popular posts. 

10. Add the new Poll service using DynamoDB 

    * /createPoll
        - POST method: takes in username (unique) of the creator, question, and response(s)1-4
        - returns a poll object in dynamodb
        - ex) {"createdBy": "someone", "question": "A question", "res1": "yes","res2": "no","res3": "","res4": ""}
        - note: the pollID generated is from epoch, and you must use this to vote 

    * /vote
        - POST method: takes a username (unique) pollID, the username of the person who created the poll, and answer 
        - creates a vote, incrementing a voteCounter for each postID
        - returns json of vote information
        - ex) {"username": "you", "pollID": [pollID], "createdBy": "someone", "answer": "yes"}

    * /getPoll
        - GET method: takes in a pollID and creator of poll
        - returns json of desired poll
        - ex) {"pollID": [pollID], "createdBy": "someone"}
        
## Notes About Project:
    * When inputting, everything is case sensitive
    * For grading purposes: We have failed to implement
        1. Service Registry Implementation
