from sqlite3.dbapi2 import DatabaseError
import hug 
import redis
import json
from user_api import post

r = redis.Redis(host='localhost', port=6379, db= 0, password=None, socket_timeout=None)

#Sets postID as key and likeCount and likedUsers as values to redis
@hug.post('/like')
def like(postID, username):
    postID = str(postID)
    if(r.exists(postID)):
        data = r.get(postID)
        data = json.loads(data)
        data['likeCount'] += 1
        if username not in data['likedUsers']:
            data['likedUsers'].append(username)
            data = json.dumps(data)
            r.set(postID, data)
        else:
            return ('User has already liked this post')
    else:
        data = {
            "likeCount": 1,
            "likedUsers": [username],
        }
        data = json.dumps(data)
        r.set(postID, data)
    if not r.exists('leader:likeCount'):
        r.zadd('leader:likeCount', {postID: 0})
    r.zincrby('leader:likeCount', 1, postID)

    r.rpush(username, postID)
    return data
    
    
#counting the number specific post.
@hug.get('/getPostLikes')
def getPostLikes(postID):
    postID = str(postID)
    if(r.exists(postID)):
        data = r.get(postID)
        data = json.loads(data)
        return data['likeCount']
    else:
        return('Post does not exist in Redis')
    

#counting the number specific post.
@hug.get('/getUserLikes')
def getUserLikes(username):
    data = r.lrange(username, 0, -1)
    if(data == None):
        return('No such username in Redis')
    return data

@hug.get('/getPopularPosts')
def PopularPost():
    return r.zrevrange('leader:likeCount', 0, 4, withscores=False)