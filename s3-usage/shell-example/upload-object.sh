objectName=testobj
file=./testobj
bucket=test
resource="/${bucket}/${objectName}"
contentType="text/plain"
dateValue=`date -R`
stringToSign="PUT\n\n${contentType}\n${dateValue}\n${resource}"
s3Key=ACCESS_KEY
s3Secret=SECRET_KEY
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`
curl -v -i -X PUT -T "${file}" \
          -H "Host: RGW_HOST" \
          -H "Date: ${dateValue}" \
          -H "Content-Type: ${contentType}" \
          -H "Authorization: AWS ${s3Key}:${signature}" \
          http://RGW_HOST:7480/${bucket}/${objectName}
