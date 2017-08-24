from flask import Flask
from flask_restplus import Resource, Api
from werkzeug.datastructures import FileStorage
from werkzeug import secure_filename
from redis import Redis
import hashlib
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from s3_file_storage import S3FileStorage

import ssl
import sys
import os

app = Flask(__name__)
api = Api(app)
redis = Redis(host='redis', port=6379)
s3store = S3FileStorage() # insecure key
s3store.setupDB('file-hashes-database')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@api.route('/upload/')
@api.expect(upload_parser)
class Upload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        filename = secure_filename(uploaded_file.filename)
        if(allowed_file(filename)):
            extension = filename.rsplit('.', 1)[1];
            hash = s3store.hashStreamAndLog(uploaded_file.stream, filename, extension)
            return {'url': os.environ['S3_BUCKET'] + '.s3.amazonaws.com/' + hash}, 201

        return { 'message': 'the file you sent could not be uploaded' }, 400


def log(arg):
    print(arg, file=sys.stderr)


@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        s3img = S3ImageStorage()
        return {'hash' : s3img.testBucket()}


if __name__ == "__main__":
    print("started python script!!!!!...");
    app.run(host="0.0.0.0", debug=True)
