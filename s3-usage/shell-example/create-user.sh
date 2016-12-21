#!/bin/bash
url="HOSTNAME:PORT"
contentType="application/json"
dateValue=`date -u +"%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="PUT\n\n${contentType}\n${dateValue}\n/admin/user"
s3Key="ACCESS_KEY"
s3Secret="SECRET_KEY"
uid="NEWUSER"
dname="NEW_USER_NO_SPACE"
caps="usage=read"
mbucks=100
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`

curl -v \
  -H "Content-Type: ${contentType}" \
  -H "Date: ${dateValue}" \
  -H "Authorization: AWS ${s3Key}:${signature}" \
  -L -X PUT "http://${url}/admin/user?format=json&uid=${uid}&display-name=${dname}&user-caps=${caps}&max-buckets=${mbucks}" \
  -H "Host: ${url}" 
