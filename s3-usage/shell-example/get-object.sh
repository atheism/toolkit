file="./down-file"
objname="testobj"
bucket=oppo
url="RGW_HOST:7480"
resource="/${bucket}/${objname}"
contentType="application/x-compressed-tar"
dateValue=`date -R`
stringToSign="GET\n\n${contentType}\n${dateValue}\n${resource}"
s3Key="ACCESS_KEY"
s3Secret="SECRET_KEY"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`
curl -o ${file} -X GET \
  -H "Host: ${url}" \
  -H "Date: ${dateValue}" \
  -H "Content-Type: ${contentType}" \
  -H "Authorization: AWS ${s3Key}:${signature}" "http://${url}/${bucket}/${objname}"
