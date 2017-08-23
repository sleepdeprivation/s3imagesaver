# s3imagesaver
Saves files on S3 with random filenames, for client access

Contains a `docker-compose.yml` that will set up a mongo/flask/redis environment that will provide an api that recieves files, mangles their filenames (hashes into a very large string), and then stores the original filename in a mongo database, and the file with mangled filename in an s3 bucket. The idea is that if the s3 bucket is properly configured, outside observers should be able to view a link if given to them, but not able to list the available files. If the encrypted filename is sufficiently long, it will be computationally infeasible to guess the filenames, rendering the files essentially hidden.
