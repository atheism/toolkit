#!/bin/bash

url="HOSTNAME:PORT"
bucket="BUCKET"
object="OBJECT"
acl="public-read"
contentType="application/xml"
dateValue=`date -u +"%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="PUT\n\n${contentType}\n${dateValue}\nx-amz-acl:${acl}\n/${bucket}/${object}?acl"
s3Key="ACCESS_KEY"
s3Secret="SECRET_KEY"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`

curl -v \
  -H "Content-Type: ${contentType}" \
  -H "Date: ${dateValue}" \
  -H "Authorization: AWS ${s3Key}:${signature}" \
  -H "x-amz-acl: $acl" \
  -L -X PUT "http://${url}/ec-test/sun-javadb-javadoc-10.6.2-1.1.i386.rpm?acl" \
  -H "Host: ${url}"
