
import unittest
from s3_file_storage import S3FileStorage
import warnings
import sys
import os
import logging



class TestS3FileStorage(unittest.TestCase):
    """
        Test the operations of the file storage system
    """

    def setUp(self):
        """
            ignore resource warning as there is some kind of error with boto
            that needs to be investigated
            afaict it only gives this warning during unitttesting, but I think
            this is only because the default behavior is to ignore ResourceWarning,
            which is reset by unittest

            https://github.com/boto/boto3/issues/454

            there's a ref in that thread to the requests library where a dev
            says that this is intended behavior for requests lib, probably
            not so much for boto tho.
        """
        warnings.simplefilter("ignore", ResourceWarning)

    def testDB(self):
        """
            Test that we can access the mongo db and write to it
        """
        s3store0 = S3FileStorage();        #insecure default key
        s3store0.setupDB('test-db-name');
        s3store0.database.table_1.delete_many({ "testing" : 123 });
        self.assertEqual(s3store0.database.table_1.count({ "testing" : 123 }), 0);
        s3store0.database.table_1.insert_one({ "testing" : 123 });
        s3store0.database.table_1.insert_one({ "testing" : 123 });
        s3store0.database.table_1.insert_one({ "testing" : 123 });
        self.assertEqual(s3store0.database.table_1.count({ "testing" : 123 }), 3);
        s3store0.database.table_1.insert_one({ "testing" : 123 });
        self.assertEqual(s3store0.database.table_1.count({ "testing" : 123 }), 4);
        s3store0.database.table_1.delete_many({ "testing" : 123 });
        self.assertEqual(s3store0.database.table_1.count({ "testing" : 123 }), 0);

    def testHashing(self):
        """
            Test that hashes with different keys hash to different values
        """
        testFileName = "assets/testfile.png";
        s3store0 = S3FileStorage();        #insecure default key
        s3store1 = S3FileStorage("key1");  #test key 1
        s3store2 = S3FileStorage("key2");  #test key 2
        hash0 = s3store0.hashFile(testFileName)
        hash1 = s3store1.hashFile(testFileName)
        hash2 = s3store2.hashFile(testFileName)
        self.assertNotEqual(hash0, hash1);
        self.assertNotEqual(hash1, hash2);
        self.assertNotEqual(hash0, hash2); #already true if the above succeeded
        #print(hash0, hash1, hash2);

    def testFileStorageAndRetrieval(self):
        testFileName = "assets/testfile.png";
        testHash = "444129db69aabab7dc2a83f9f38fb807dd456c411fd21dae0b24348f1598b314";
        s3store0 = S3FileStorage();        # insecure default key
        s3store0.setupDB('test-db-2');
        s3store0.database.fileHashes.delete_many({}); # wipe the collection
        s3store0.hashFileAndLog(testFileName)
        hashDict = s3store0.getHashByFilename(testFileName)
        self.assertEqual(testHash, hashDict['hashedFile'])


if __name__ == '__main__':
    unittest.main()
