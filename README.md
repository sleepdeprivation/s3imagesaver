# s3imagesaver
Saves files on S3 with random filenames, for client access

Contains a `docker-compose.yml` that will set up a mongo/flask/redis environment that will provide an api that recieves files, hashes the contents into a large hex string, and then stores the original filename and hash in a mongo database, and the file with the hash as its filename in an s3 bucket. The idea is that if the s3 bucket is properly configured, outside observers should be able to view a link if given to them, but not able to list the available files. If the encrypted filename is sufficiently long, it will be computationally infeasible to guess the filenames, rendering the files essentially hidden.

## Basic Usage

A flask api is provided with an `/upload/` POST route which will allow uploads of arbitrary images (must have an extension that looks like an image). The upload will be saved in the specified s3 bucket and will return a url. The original image name will also be saved in the mongo database.

# Security Warning!

This is by no means production ready. Just off the top of my head, file sizes should be checked (don't know if flask/restplus/whatever does this by default). Also many things are not generic enough.

In addition the key used for hashing the filenames is not secure, and should not be used in production. In the future this should be moved to `.env` as an environment variable and a warning should be given or an error thrown if it doesn't get changed.

## Installing

You will need `docker` and `docker-compose`

## S3 Creds

Provide S3 creds as environment variables or in the .env file, and example of which is given as .env.example

## testing

Currently tests can be performed by doing `docker-compose up` and then while the image is up run `docker exec -it python_api python -m unittest discover`.
