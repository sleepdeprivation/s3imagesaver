from flask import Flask
from redis import Redis
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import sys

def log(arg):
    print(arg, file=sys.stderr)


def testDB():
    log("testing db...");
    client = MongoClient('database', 27017)
    try:
       # The ismaster command is cheap and does not require auth.
       client.admin.command('ismaster')
       log("successful connection!");
    except ConnectionFailure:
       log("Server not available")

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    log("going to test db...");
    testDB();
    log("completed db");
    count = redis.incr('hits')
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    print("started python script!!!!!...");
    app.run(host="0.0.0.0", debug=True)
