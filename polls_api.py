import boto3
import hug
import requests
import json
import time
from botocore.exceptions import ClientError



@hug.post('/createPoll')
def create_poll(createdBy, question, res1, res2, res3, res4, dynamodb=None):
    print('Creating Poll...')
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

    table = dynamodb.Table('Polls')

    #user time to assign pollID's
    epoch = int(time.time())
    pollID = epoch
    print(pollID)

    print('createdBy:', createdBy, 'question:', question, 'res1:', res1, 'res2:', res2, 'res3:', res3, 'res4:', res4)
    response = table.put_item(
       Item={
            'pollID': pollID,
            'createdBy': createdBy,
            'poll_details': {
                'question': question,
                'res1': res1,
                'voteCount1': 0,
                'res2': res2,
                'voteCount2': 0,
                'res3': res3,
                'voteCount3': 0,
                'res4': res4,
                'voteCount4': 0,
            },
            'votedUsers': ''
        }
    )
    return response

@hug.put('/vote')
def vote(username, pollID, createdBy, answer, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

    table = dynamodb.Table('Polls')
    try:
        response = table.get_item(Key={'pollID': pollID, "createdBy": createdBy})

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            res1_total = response['Item']['poll_details']['voteCount1']
            res2_total = response['Item']['poll_details']['voteCount2']
            res3_total = response['Item']['poll_details']['voteCount3']
            res4_total = response['Item']['poll_details']['voteCount4']
            if username in response['Item']['votedUsers']:
                return 'User has already voted...'
            else:
                print(response['Item']['votedUsers'])
                newVotedString = response['Item']['votedUsers'] + username +','
                print(newVotedString)
            if response['Item']['poll_details']['res1'] == answer:
                res1_total = response['Item']['poll_details']['voteCount2'] + 1
            elif response['Item']['poll_details']['res2'] == answer:
                res2_total = response['Item']['poll_details']['voteCount2'] + 1
            elif response['Item']['poll_details']['res3'] == answer:
                res3_total = response['Item']['poll_details']['voteCount3'] + 1
            elif response['Item']['poll_details']['res4'] == answer:
                res4_total = response['Item']['poll_details']['voteCount4'] + 1;

            print('Updating Poll...') #cc
            update = table.update_item(
                Key = {
                    'pollID': pollID,
                    'createdBy': createdBy
                },
                UpdateExpression = 'set poll_details.voteCount1=:v1,\
                                    poll_details.voteCount2=:v2,\
                                    poll_details.voteCount3=:v3,\
                                    poll_details.voteCount4=:v4,\
                                    votedUsers=:vu',
                ExpressionAttributeValues={
                    ':v1': res1_total,
                    ':v2': res2_total,
                    ':v3': res3_total,
                    ':v4': res4_total,
                    ':vu': newVotedString,
                },
                ReturnValues='UPDATED_NEW'
            )
            return update
        else:
            print('Error')
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']

@hug.get('/getPoll')
def get_poll(pollID, createdBy, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
    table = dynamodb.Table('Polls')
    response = table.get_item(Key={'pollID': pollID, "createdBy": createdBy})
    return response