from flask import Flask
from flask_restplus import Resource, Api
from redis import Redis
import hashlib
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from oauth_verify import authorized
from image_storage import S3ImageStorage

import ssl
from hashlib import blake2b
import sys
import os

def log(arg):
    print(arg, file=sys.stderr)

client = MongoClient('database', 27017)

def testDB():
    log("testing db...");
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
        s3img = S3ImageStorage()
        return {'hash' : s3img.testBucket()}


if __name__ == "__main__":
    print("started python script!!!!!...");
    testDB();
    app.run(host="0.0.0.0", debug=True)
