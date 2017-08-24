
import os
import s3fs
from hashlib import blake2b

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import pprint;

class S3FileStorage():
    """
        Class for hashing files and storing them on s3 with hashed filenames
        The true filename is stored in a database with the associated hashname
        for recovery and indexing
    """

    def __init__(self, key=None):
        """
            Provide a key for hashing, if none is provided an easy one is set
        """
        if(key is None):
            self.key = b'THIS NEEDS TO BE A REASONABLY LARGE RANDOM KEY';
        else:
            self.setKey(key);

    def setKey(self, key):
        """
            Set the salt/key used for the hashing algorithm, expects a string
        """
        self.key = key.encode()

    def setupDB(self, dbname):
        """
            Set up the mongo connection and attempt a simple operation
            raise a ConnectionRefusedError if the connection failed
            Also set self.client to the mongo client and self.database to the
            provide database name
        """
        self.client = MongoClient('database', 27017); # "database" as defined in compose yml file
        try:
           # The ismaster command is cheap and does not require auth.
           self.client.admin.command('ismaster')
           print("Mongo connection successfully established!");
        except ConnectionFailure:
            print("Mongo connection failed. Raising exception!");
            raise ConnectionRefusedError("Mongo Server not detected!");
        self.database = self.client[dbname];
        return self.database;

    def logFileToDB(self, filename, hashedFileContents):
        """
            log the mapping between cleartext filename and hashed filecontents
            to the database
            return the mongo db identifier of the inserted object
        """
        return self.database.fileHashes.insert_one({
                            "originalFilename" : filename,
                            "hashedFile" : hashedFileContents
            });

    def hashBytes(self, filebytes):
        """
            take the provided bytes and hash them using blake, salting with
            the key provided
        """
        h = blake2b(self.key, digest_size=32)
        h.update(filebytes)
        return h.hexdigest()

    def getFileContents(self, filename):
        """
            Read the given local filename into an array (?) of bytes and return it
        """
        with open(filename, "rb") as f:
            bytes = f.read()
        return bytes;

    def hashFile(self, filename):
        """
            Go get the file contents and hash them and return the hash
        """
        return self.hashBytes(self.getFileContents(filename))

    def writeFileToS3Bucket(self, sourceFile, hashedFile):
        """
            Write a localfile given by originalFilename to hashedFilename in the s3
            bucket. S3 creds are provided by environment variables
        """
        bucket_name = os.environ['S3_BUCKET'];
        s3 = s3fs.S3FileSystem(anon=False, key=os.environ['S3_KEY'], secret=os.environ['S3_SECRET'])
        s3.put(sourceFile, bucket_name + "/" + hashedFile);

    def writeBytesToS3Bucket(self, bytes, hashedFile, meta):
        """
            write the bytes given in bytes to s3
        """
        bucket_name = os.environ['S3_BUCKET'];
        s3 = s3fs.S3FileSystem(anon=False, key=os.environ['S3_KEY'], secret=os.environ['S3_SECRET'])
        remoteFile = bucket_name + "/" + hashedFile;
        with s3.open(remoteFile, mode='wb') as f:
            f.write(bytes);

        s3.setxattr(remoteFile, copy_kwargs=meta)

    def hashFileAndLog(self, filename):
        """
            Perform the hash on the contents of the file, then write the file to
            the s3 bucket under the hashed filename
        """
        hashedFile = self.hashFile(filename);
        self.writeFileToS3Bucket(filename, hashedFile);
        self.logFileToDB(filename, hashedFile);

    def hashStreamAndLog(self, stream, filename, extension):
        """
            Given a stream hash it and send it to s3
            Then log it in the mongodb
            This function preserves the extension in an ugly way,
            not sure that's the right thing to do...
            Now it assumes an image! Getting less and less general...
        """
        bytes = stream.read();
        hash = self.hashBytes(bytes);
        meta = {'ContentType': 'image/'+extension}
        self.writeBytesToS3Bucket(bytes, hash + "." + extension, meta);
        self.logFileToDB(filename, hash + "." + extension);
        # unnecessary to hit the db again, but makes me feel better what with
        # the file extension hacks above
        return self.getHashByFilename(filename)['hashedFile'];


    def getHashByFilename(self, filename):
        """
            Check the mongodb for the given filename and return its hash
        """
        hashDict = self.database.fileHashes.find_one({"originalFilename" : filename });
        return hashDict;

    def deleteFileByHash(self, filename):
        pass
