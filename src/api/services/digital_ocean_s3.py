import logging
from django.conf import settings
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class S3Service:
    def __init__(
        self,
        bucket="Scoolarc",
    ):
        self.s3_client = settings.S3_CLIENT
        self.bucket = bucket

    def get_bucket_and_s3_key(self, s3_url):
        parsed_url = urlparse(s3_url)
        bucket = parsed_url.netloc
        key = parsed_url.path.lstrip("/")
        return bucket, key

    def upload_file(self, file_obj, s3_key, is_public=True):
        """
        Uploads a file directly from an HTTP request to a specific folder in DigitalOcean Spaces.
        :param file_obj: The file object from the HTTP request (e.g., request.FILES['file'])
        :param s3_key: The unique file name in the space
        :param is_public: Flag to set the file as public (if True, it will be accessible via a public URL)
        :return: The URL for the uploaded file (public or private)
        """
        try:
            # Upload the file directly from the request
            self.s3_client.upload_fileobj(file_obj, self.bucket, s3_key)

            # If the file is public, set the ACL to public-read
            if is_public:
                self.s3_client.put_object_acl(
                    Bucket=self.bucket, Key=s3_key, ACL="public-read"
                )
                logger.info(f"File uploaded and set to public: {s3_key}")
            else:
                logger.info(f"File uploaded successfully (private): {s3_key}")

            # Return the URL of the uploaded file
            if is_public:
                # Construct the public URL for the uploaded file
                file_url = f"{settings.OBJECT_STORAGE_URL}/{self.bucket}/{s3_key}"
            else:
                file_url = f"s3://{self.bucket}/{s3_key}"

            return file_url
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            raise Exception(f"Error uploading file: {e}")

    def generate_presigned_url(self, s3_url, expiration=3600):
        """
        Generates a presigned URL to access the uploaded file from the Space.
        :param bucket: The name of the Space
        :param s3_key: The object name in the space
        :param expiration: Time in seconds for which the URL is valid
        :return: Presigned URL
        """
        try:
            bucket, key = self.get_bucket_and_s3_key(s3_url)
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=expiration,
            )
            logger.info(f"Generated presigned URL for {s3_url}")
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {e}")
            raise Exception(f"Error generating presigned URL: {e}")

    def generate_presigned_url_for_upload(self, key, content_type, expiration=3600):
        """
        Generates a presigned URL to upload file from the Space.
        :param key: The object fullpath and name in the space
        :param expiration: Time in seconds for which the URL is valid
        :return: Presigned URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.bucket,
                    "Key": key,
                    "ContentType": content_type,
                },
                ExpiresIn=expiration,
            )
            logger.info("Generated presigned URL for file upload")
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {e}")
            raise Exception(f"Error generating presigned URL: {e}")

    def make_presigned_file_public(self, key):
        """
        Makes a file in the S3 bucket public.
        :param s3_key: The object name (key) in the bucket to be made public
        :return: Success message or raises exception
        """
        try:
            self.s3_client.put_object_acl(
                Bucket=self.bucket,
                Key=key,
                ACL="public-read",
            )
            logger.info(f"File {key} is now public.")
            return f"{settings.OBJECT_STORAGE_URL}/{self.bucket}/{key}"
        except Exception as e:
            logger.error(f"Error making file public: {e}")

    def delete_file(self, s3_url):
        """
        Deletes a file from the S3 bucket.
        :param s3_key: The object name (key) in the bucket to be deleted
        :return: Success message or raises exception
        """
        try:
            # Delete the file from the bucket
            bucket, key = self.get_bucket_and_s3_key(s3_url)
            self.s3_client.delete_object(Bucket=bucket, Key=key)
            logger.info(f"File {key} deleted successfully.")
            return f"File {key} deleted successfully."
        except Exception as e:
            logger.error(f"Error deleting file from S3: {e}")
            raise Exception(f"Error deleting file: {e}")
