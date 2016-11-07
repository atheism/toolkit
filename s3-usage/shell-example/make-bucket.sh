bucket="test"  
dateValue=`date -R`  
#dateValue=$(curl -v --silent http://RGW_HOST:7480 2>&1 | grep Date | sed -e 's/< Date: //')  
echo $dateValue
resource="/${bucket}/"  
contentType="application/octet-stream"  
stringToSign="PUT\n\n${contentType}\n${dateValue}\n${resource}"  
echo -en $stringToSign
#stringToSign="PUT\n\n\n${dateValue}\n${resource}"  
s3Key=ACCESS_KEY
s3Secret=SECRET_KEY
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`  
echo ${signature}
curl -v -X PUT "http://RGW_HOST:7480/${bucket}/" -H "Host: http://RGW_HOST:7480" -H "Date: ${dateValue}" -H "Authorization: AWS ${s3Key}:${signature}" -H "Content-Type: ${contentType}"
