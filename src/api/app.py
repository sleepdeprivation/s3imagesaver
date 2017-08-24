from flask import Flask
from flask_restplus import Resource, Api
from redis import Redis
import hashlib
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from s3_file_storage import S3FileStorage

import ssl
import sys
import os

def log(arg):
    print(arg, file=sys.stderr)

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
    app.run(host="0.0.0.0", debug=True)
