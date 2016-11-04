import java.io.ByteArrayInputStream;
import java.io.File;
import java.util.List;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.util.StringUtils;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.GeneratePresignedUrlRequest;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.S3ObjectSummary;

import com.amazonaws.ClientConfiguration;
import com.amazonaws.Protocol;

class OfficialUsage {
	public static void main(String []args) {
	
		String accessKey = "admin";
		String secretKey = "admin";
		
		// create connection
		AWSCredentials credentials = new BasicAWSCredentials(accessKey, secretKey);
		AmazonS3 conn = new AmazonS3Client(credentials);
		conn.setEndpoint("http://10.0.101.68:7480");
	
		// list bucket in this account
		List<Bucket> buckets = conn.listBuckets();
		for (Bucket bucket : buckets) {
		        System.out.println(bucket.getName() + "\t" +
		                StringUtils.fromDate(bucket.getCreationDate()));
		}


		// make a new bucket. success if existing
		Bucket bucket = conn.createBucket("my-new-bucket");
	
		// upload some file and list objects in a bucket
		// generate hello.txt and secret_plans.txt
		ByteArrayInputStream input = new ByteArrayInputStream("Hello World!".getBytes());
		conn.putObject(bucket.getName(), "hello.txt", input, new ObjectMetadata());
		ByteArrayInputStream secretinput = new ByteArrayInputStream("My secret!".getBytes());
		conn.putObject(bucket.getName(), "secret_plans.txt", secretinput, new ObjectMetadata());
		// set ACL
		conn.setObjectAcl(bucket.getName(), "hello.txt", CannedAccessControlList.PublicRead);
		conn.setObjectAcl(bucket.getName(), "secret_plans.txt", CannedAccessControlList.Private);
		// download file
		conn.getObject(
		        new GetObjectRequest(bucket.getName(), "hello.txt"),
		        new File("./hello.txt")
		);

		// list objects in a bucket 
		ObjectListing objects = conn.listObjects(bucket.getName());
		do {
	        	for (S3ObjectSummary objectSummary : objects.getObjectSummaries()) {
	                	System.out.println(objectSummary.getKey() + "\t" +
	                        	objectSummary.getSize() + "\t" +
	                        	StringUtils.fromDate(objectSummary.getLastModified()));
	        	}
	        	objects = conn.listNextBatchOfObjects(objects);
		} while (objects.isTruncated());

		// create and delete a file in bucket
		ByteArrayInputStream byeinput = new ByteArrayInputStream("Good bye!".getBytes());
		conn.putObject(bucket.getName(), "goodbye.txt", byeinput, new ObjectMetadata());
		conn.deleteObject(bucket.getName(), "goodbye.txt");

		// create an empty bucket and delete it.
		Bucket bucketdel = conn.createBucket("for-delete");
		conn.deleteBucket(bucketdel.getName());

	}
}
