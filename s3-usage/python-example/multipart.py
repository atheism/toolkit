#!/usr/bin/env python
import math, os
import boto
import boto.s3.connection
from filechunkio import FileChunkIO

CONS_AK = 'ACCESS_KEY'
CONS_SK = 'SECRET_KEY'

# Connect to S3
c = boto.connect_s3(
            aws_access_key_id=CONS_AK,
            aws_secret_access_key=CONS_SK,
            host='HOST',
            port=7480,
            is_secure=False,
            calling_format=boto.s3.connection.OrdinaryCallingFormat()
        )

# b = c.get_bucket('mybucket')
b = c.create_bucket('test-bucket')

# Local file path
source_path = './local-large-file'
source_size = os.stat(source_path).st_size

# Create a multipart upload request
mul_key = 'my-multi-obj'
header = {
    'x-amz-meta-joseph': 'Multipart test'
}
mp = b.initiate_multipart_upload(mul_key, headers=header)

# Use a chunk size of 20 MiB (feel free to change this)
chunk_size = 20971520
chunk_count = int(math.ceil(source_size / float(chunk_size)))

# Send the file parts, using FileChunkIO to create a file-like object
# that points to a certain byte range within the original file. We
# set bytes to never exceed the original file size.
for i in range(chunk_count):
    offset = chunk_size * i
    bytes = min(chunk_size, source_size - offset)
    with FileChunkIO(source_path, 'r', offset=offset,
            bytes=bytes) as fp:
        mp.upload_part_from_file(fp, part_num=i + 1)

# Finish the upload
mp.complete_upload()
