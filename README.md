# s3imagesaver
Saves files on S3 with random filenames, for client access

Contains a `docker-compose.yml` that will set up a mongo/flask/redis environment that will provide an api that recieves files, hashes the contents into a large hex string, and then stores the original filename and hash in a mongo database, and the file with mangled filename in an s3 bucket. The idea is that if the s3 bucket is properly configured, outside observers should be able to view a link if given to them, but not able to list the available files. If the encrypted filename is sufficiently long, it will be computationally infeasible to guess the filenames, rendering the files essentially hidden.

# installing

You will need `docker` and `docker-compose`

# S3 Creds

Provide S3 creds as environment variables or in the .env file, and example of which is given as .env.example

# testing

Currently tests can be performed by doing `docker-compose up` and then while the image is up run `docker exec -it python_api python -m unittest discover`.
