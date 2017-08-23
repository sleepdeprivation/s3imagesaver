
import unittest

class TestStringMethods(unittest.TestCase):

    def testBucketCreation(self):
        s3 = s3fs.S3FileSystem(anon=False, key=os.environ['S3_KEY'], secret=os.environ['S3_SECRET'])
        with s3.open(os.environ['S3_BUCKET'] + "/testfile_klasjflkjasflk", 'wb') as file:
            file.write(b'helloworld');
        with s3.open(os.environ['S3_BUCKET'] + "/testfile_klasjflkjasflk", 'rb') as file:
            assertEqual(file.read() == b'helloworld')

if __name__ == '__main__':
    unittest.main()
