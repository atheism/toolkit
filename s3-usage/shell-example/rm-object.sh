objectName=testobj
file=./testobj
bucket=test
resource="/${bucket}/${objectName}"
contentType="application/plain"
dateValue=`date -R`
stringToSign="DELETE\n\n\n${dateValue}\n${resource}"
echo -en $stringToSign
s3Key=ACCESS_KEY
s3Secret=SECRET_KEY
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`
curl -v -i -X DELETE \
          -H "Host: RGW_HOST:7480" \
          -H "Date: ${dateValue}" \
          -H "Authorization: AWS ${s3Key}:${signature}" \
          http://RGW_HOST:7480/${bucket}/${objectName}
