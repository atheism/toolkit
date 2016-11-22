url="HOST:PORT"
contentType="application/x-compressed-tar"
dateValue=`date -R`
stringToSign="GET\n\n${contentType}\n${dateValue}\n/admin/user"
uid="UID"
s3Key="ACCESS_KEY"
s3Secret="SECRET_KEY"
signature=`echo -en ${stringToSign} | openssl sha1 -hmac ${s3Secret} -binary | base64`
curl -X GET \
    -H "Host: ${url}" \
    -H "Date: ${dateValue}" \
    -H "Content-Type: ${contentType}" \
    -H "Authorization: AWS ${s3Key}:${signature}" "http://${url}/admin/user?uid=${UID}"
