import boto3

s3 = boto3.client('s3')

# List all buckets
response = s3.list_buckets()

print("Buckets:")
for bucket in response['Buckets']:
    print(f"- {bucket['Name']}")

# Count objects in a specific bucket
bucket_name = 'my-static-site-bucket-2025'
s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(bucket_name)

object_count = sum(1 for _ in bucket.objects.all())
print(f"\nTotal objects in {bucket_name}: {object_count}")
