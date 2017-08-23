
import os
import s3fs

class S3ImageStorage():

    def logFileToDB(self, meta):
        db = client['file-db'];
        db.insert_one(meta);

    def hashFile(self, filebytes):
        h = blake2b(key=b'THIS NEEDS TO BE A REASONABLY LARGE RANDOM KEY', digest_size=64)
        h.update(filebytes)
        return h.hexdigest()

    def getFileContents(self):
        with open("assets/testfile.png", "rb") as f:
            bytes = f.read()
        return hashFile(bytes);
