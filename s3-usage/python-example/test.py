import boto
import boto.s3.connection
access_key = 'ACCESS_KEY'
secret_key = 'SECRET_KEY'

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 'RGW_HOST',
        port = 7480,
        is_secure=False,               # uncomment if you are not using ssl
        calling_format = boto.s3.connection.OrdinaryCallingFormat()
        )

for bucket in conn.get_all_buckets():
        print "{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
        )


bucket = conn.create_bucket('my-new-bucket')

for key in bucket.list():
        print "{name}\t{size}\t{modified}".format(
                name = key.name,
                size = key.size,
                modified = key.last_modified,
                )

#conn.delete_bucket(bucket.name)

key = bucket.new_key('hello.txt')
key.set_contents_from_string('Hello World!')

hello_key = bucket.get_key('hello.txt')
hello_key.set_canned_acl('public-read')
plans_key = bucket.get_key('secret_plans.txt')
plans_key.set_canned_acl('private')

key = bucket.get_key('2.map')
key.get_contents_to_filename('./map.2')

bucket.delete_key('hello.txt')
