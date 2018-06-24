from pymongo import MongoClient
from datetime import datetime

from sender import PyMS
import requests
import sys

client = MongoClient('mongodb://heroku_6k3891bs:73gsp23uusn3j7adgsk7fr75pg@ds263590.mlab.com:63590/heroku_6k3891bs')
db = client['heroku_6k3891bs']
user_collection = db['user']

if len(sys.argv) != 3:
    print('Usage: `python3 reminder_sender.py <gmail user> <gmail pass>`')
    sys.exit(1)

pyms = PyMS(username=sys.argv[1], password=sys.argv[2])
pyms.connect()

carriers = {
    'Sprint': '@messaging.sprintpcs.com',
    'Verizon': '@vtext.com',
    'AT&T': '@txt.att.net',
    'T-Mobile': '@tmomail.net'
}

#    _____                _           _
#   |  __ \              (_)         | |
#   | |__) |___ _ __ ___  _ _ __   __| | ___ _ __ ___
#   |  _  // _ \ '_ ` _ \| | '_ \ / _` |/ _ \ '__/ __|
#   | | \ \  __/ | | | | | | | | | (_| |  __/ |  \__ \
#   |_|  \_\___|_| |_| |_|_|_| |_|\__,_|\___|_|  |___/
#
#
reminder_collection = db['reminder']
reminders = reminder_collection.find({'sent': False, 'timeToSend': {'$lte': datetime.utcnow()}})
for reminder in reminders:
    user = user_collection.find_one({'_id': reminder['userId']})
    pyms.send_sms(str(int(user['phone'])), carriers[user['carrier']], reminder['content'])
    reminder_collection.update({'_id': reminder['_id']}, {'$set': {'sent': True}})
    print('Sending "' + reminder['content'] + '" to ' + user['username'])

#
#       /\
#      /  \   _ __   ___  _ __  _   _ _ __ ___   ___  _   _ ___
#     / /\ \ | '_ \ / _ \| '_ \| | | | '_ ` _ \ / _ \| | | / __|
#    / ____ \| | | | (_) | | | | |_| | | | | | | (_) | |_| \__ \
#   /_/___ \_\_| |_|\___/|_| |_|\__, |_| |_| |_|\___/ \__,_|___/
#   |  __ \              (_)     __/ | |
#   | |__) |___ _ __ ___  _ _ __|___/| | ___ _ __ ___
#   |  _  // _ \ '_ ` _ \| | '_ \ / _` |/ _ \ '__/ __|
#   | | \ \  __/ | | | | | | | | | (_| |  __/ |  \__ \
#   |_|  \_\___|_| |_| |_|_|_| |_|\__,_|\___|_|  |___/
#
#
anonymous_reminder_collection = db['anonymous-reminder']
anonymous_reminders = anonymous_reminder_collection.find(
    {'sent': False, 'timeToSend': {'$lte': datetime.utcnow()}})

for reminder in anonymous_reminders:
    pyms.send_sms(str(int(reminder['phone'])), carriers[reminder['carrier']], reminder['content'])
    anonymous_reminder_collection.update({'_id': reminder['_id']}, {'$set': {'sent': True}})
    print('Sending "' + reminder['content'] + '" to anonymous user.')

#
#     _____       _                   _       _   _
#    / ____|     | |                 (_)     | | (_)
#   | (___  _   _| |__  ___  ___ _ __ _ _ __ | |_ _  ___  _ __  ___
#    \___ \| | | | '_ \/ __|/ __| '__| | '_ \| __| |/ _ \| '_ \/ __|
#    ____) | |_| | |_) \__ \ (__| |  | | |_) | |_| | (_) | | | \__ \
#   |_____/ \__,_|_.__/|___/\___|_|  |_| .__/ \__|_|\___/|_| |_|___/
#                                      | |
#                                      |_|
subscription_collection = db['subscription']
subscriptions = subscription_collection.find()

for subscription in subscriptions:
    send_time = subscription['timeToSend'].split(':')
    send_hour = int(send_time[0])
    send_minute = int(send_time[1])
    send_minutes = send_hour * 60 + send_minute

    hour = datetime.now().hour
    minute = datetime.now().minute
    reminder_minutes = hour * 60 + minute

    if send_minutes == reminder_minutes:
        message = requests.get('https://wrr-webdev-project-node.herokuapp.com/api/recurring/example/' + subscription['recurringReminder']).text
        user = user_collection.find_one({'_id': subscription['userId']})
        pyms.send_sms(str(int(user['phone'])), carriers[user['carrier']], message)

pyms.disconnect()
client.close()
