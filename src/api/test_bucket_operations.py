
import unittest
import s3fs
import os
import warnings

class TestBucketOperations(unittest.TestCase):
    """
        Ensure we can read and write to the S3 bucket
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

    def testEnvironmentVariables(self):
        """
            test that environment vars have been set properly, else all other
            tests will be useless
        """
        self.assertNotEqual(os.environ['S3_KEY'], 'keyhere')
        self.assertEqual(os.environ['TEST_ENV_VAR'], 'testing')

    def testFileCreation(self):
        """
            make a file, read/write, delete it, check that it doesn't exist
        """
        filename = os.environ['S3_BUCKET'] + "/testfile_klasjflkjasflk";
        s3 = s3fs.S3FileSystem(anon=False, key=os.environ['S3_KEY'], secret=os.environ['S3_SECRET'])
        if(s3.exists(filename)):
            s3.rm(filename)
        with s3.open(filename, 'wb') as file:
            file.write(b'helloworld');
        with s3.open(filename, 'rb') as file:
            self.assertEqual(file.read(), b'helloworld')
        if(s3.exists(filename)):
            s3.rm(filename)
        self.assertFalse(s3.exists(filename));



if __name__ == '__main__':
    unittest.main()
