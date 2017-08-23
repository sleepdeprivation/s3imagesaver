
import unittest
import s3fs
import os

class TestBucketOperations(unittest.TestCase):

    def testEnvironmentVariables(self):
        self.assertNotEqual(os.environ['S3_KEY'], 'keyhere')
        self.assertEqual(os.environ['TEST_ENV_VAR'], 'testing')

    def testFileCreation(self):
        s3 = s3fs.S3FileSystem(anon=False, key=os.environ['S3_KEY'], secret=os.environ['S3_SECRET'])
        with s3.open(os.environ['S3_BUCKET'] + "/testfile_klasjflkjasflk", 'wb') as file:
            file.write(b'helloworld');
        with s3.open(os.environ['S3_BUCKET'] + "/testfile_klasjflkjasflk", 'rb') as file:
            self.assertEqual(file.read() == b'helloworld')

if __name__ == '__main__':
    unittest.main()
