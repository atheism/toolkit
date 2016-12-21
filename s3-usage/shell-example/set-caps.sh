#!/bin/bash
url="10.0.101.69:7480"
contentType="application/json"
dateValue=`date -u +"%a, %d %b %Y %H:%M:%S GMT"`
stringToSign="PUT\n\n${contentType}\n${dateValue}\n/admin/user"
s3Key="ACCESS_KEY"
s3Secret="SECRET_KEY"
uid="UID"
caps="usage=read,write;users=*"

signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`

curl -v \
  -H "Content-Type: ${contentType}" \
  -H "Date: ${dateValue}" \
  -H "Authorization: AWS ${s3Key}:${signature}" \
  -L -X PUT "http://${url}/admin/user?caps&uid=${uid}&user-caps=${caps}" \
  -H "Host: ${url}" 
