from flask import Flask
from flask_restplus import Resource, Api
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
       log("Mongo connection successfully established!");
    except ConnectionFailure:
        log("Mongo connection failed. Raising exception!");
        raise ConnectionRefusedError("Mongo Server not detected!");

app = Flask(__name__)
api = Api(app)
redis = Redis(host='redis', port=6379)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == "__main__":
    print("started python script!!!!!...");
    testDB()
    app.run(host="0.0.0.0", debug=True)
