import boto3

"""
S3 Bucket Script to interact with AWS S3

Note: 
    In order to use you need to have / create IAM User and Role for programmatic access.
    Create a ~/.boto file with the below syntax:
    [Credentials]
    AWS_ACCESS_KEY_ID = "Your Access Key"
    AWS_SECRET_ACCESS_KEY = "Your Secret Key"


    create_a_bucket : create a new bucket
    access_a_bucket : access a bucket
    delete_a_bucket : delete a bucket
    upload_a_file : upload a file


"""

# Create an S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME
)

BUCKET_NAME="your_bucket_name"
FILE_PATH="path/to/your/local/file"
OBJECT_NAME="path/to/your/file/in/s3" 

#Create a new bucket
def create_a_bucket(bucket_name,region):
    try:
        # Create the bucket with region
        s3.create_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created successfully in {region}")

    except Exception as e:
        print(f"Error creating bucket: {e}")


#Access a bucket
def access_a_bucket(bucket_name):
    try:
        bucket = s3.get_bucket(bucket_name)
        print(f"Bucket {bucket} exists")
        print(bucket.list)
    except Exception as e:
        print(f"Error accessing bucket: {e}")


#Delete a bucket
def delete_a_bucket(bucket_name):
    #Delete a bucket
    try:
        s3.delete_bucket(bucket_name)
        print(f"{BUCKET_NAME} Bucket Deleted Successfully")
    except Exception as e:
        print(f"Error deleting bucket: {e}")


def upload_a_file(bucket_name):
    # Upload the file
    try:
        s3.upload_file(FILE_PATH, BUCKET_NAME, OBJECT_NAME)
        print(f"File uploaded successfully to s3://{BUCKET_NAME}/{OBJECT_NAME}")
    except Exception as e:
        print(f"Error uploading file: {e}")






