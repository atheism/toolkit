# -*- coding:utf-8 -*-
import boto
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import SubdomainCallingFormat
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
import sys
import tempfile


import requests
import urlparse 


class Object(object):
    def __init__(self, name, md5, size, headers):
        self.name = name
        self.size = int(size)
        self.headers = headers
        
    def set_headers(self, headers):
        self.headers = headers
   
class LocalCopy(object):
    def __init__(self, obj_name, path, path_is_temp):
        self.obj_name = obj_name
        self.path = path
        self.path_is_temp = path_is_temp
    def remove(self):
        if ((self.path_is_temp == True) and (self.path != None)):
            os.unlink(self.path)
        self.path = None
        self.path_is_temp = False
    def __del__(self):
        self.remove()
  
class S3Store():
    def __init__(self, host, bucketname, akey, skey):
        self.host = host
        self.bucket_name = bucketname

        self.conn = S3Connection(
                calling_format=OrdinaryCallingFormat(),
                host=self.host,
                port=80,
                is_secure=False,
                aws_access_key_id=akey,
                aws_secret_access_key=skey)

        self.bucket = self.conn.lookup(self.bucket_name)
        if (self.bucket == None):            
            raise

    def locate_object(self, obj):
        k = self.bucket.get_key(obj.name)
        if (k == None):
            return None
        return Object(obj.name, None, k.size, None)

    def upload(self, local_copy, obj):
        k = Key(self.bucket)
        k.key = obj.name
        k.set_contents_from_filename(local_copy.path, obj.headers)
        k.set_canned_acl('public-read', None)

            
def http_meta_to_headers(rest_headers):
    headers = {}
    if rest_headers is not None:
        if rest_headers['cache-control'] is not None:
            headers['Cache-Control'] = rest_headers['cache-control']
        if rest_headers['content-type'] is not None:
            headers['Content-Type'] = rest_headers['content-type']
    return headers
 
    
class HttpUrlStore():
    def __init__(self, bucketname, urlpath, srcheaders):
        self.srcheaders = srcheaders
        self.bucket_name = bucketname,
        self.urlpath = urlpath
    
    def get_object(self):
        obj_name = urlparse.urlparse(self.urlpath).path
        return Object(urllib2.url2pathname(obj_name), None, 0, None)
    
    def make_local_copy(self, obj):
        # req_headers={'Host':'abc.com'};
        result = requests.get(self.urlpath, headers=self.srcheaders, timeout=180, allow_redirects=False)
         
        if not result.ok:
            return None
        obj.headers = http_meta_to_headers(result.headers)
        
        temp_file = tempfile.NamedTemporaryFile(mode='w+b', delete=False).name
        try:
            with open(temp_file, 'wb') as download_file:
                download_file.write(result.content)  # TODO big file process
        except Exception, e:
            os.unlink(temp_file)
            raise e
        return LocalCopy(obj.name, temp_file, True)
 

def handle_url(bucket_name, urlpath, host, akey, skey, srcheaders):
    print(bucket_name)
    print(urlpath)
    try:
        src = HttpUrlStore(bucket_name, urlpath, srcheaders)
    except Exception, e:
        raise e
    try:
        dst = S3Store(host, bucket_name, akey, skey)
    except Exception, e:
        raise e

    try:
        sobj = src.get_object()
    except StopIteration:
        exit(1)
    
    upload = True      
    if dst.locate_object(sobj) is not None:
        upload = False    

    if (upload):
        local_copy = src.make_local_copy(sobj)
        if local_copy is None:
            exit(1)
        try:
            dst.upload(local_copy, sobj)
        finally:
            local_copy.remove()
    
if __name__ == '__main__':
    bucket_name = 'bucket_name'
    urlpath = 'http://172.16.0.220/arch.png'
    host = '172.16.0.32'
    akey = 'admin'
    skey = 'admin'
    handle_url(bucket_name, urlpath, host, akey, skey, srcheaders={})

