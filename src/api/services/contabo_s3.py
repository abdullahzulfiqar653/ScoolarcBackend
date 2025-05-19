import datetime
import hashlib
import hmac
import requests
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


class ContaboObjectStorageService:
    def __init__(self, access_key, secret_key, region, bucket_name, endpoint_url):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url.rstrip("/")

    def _sign(self, key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def _get_signature_key(self, date_stamp, service="s3"):
        k_date = self._sign(("AWS4" + self.secret_key).encode("utf-8"), date_stamp)
        k_region = self._sign(k_date, self.region)
        k_service = self._sign(k_region, service)
        return self._sign(k_service, "aws4_request")

    def _get_host(self):
        return self.endpoint_url.replace("https://", "")

    def _get_canonical_uri(self, key):
        return f'/{self.bucket_name}/{key}'

    def upload_file(self, file_obj, s3_key, is_public=False):
        try:
            payload = file_obj.read()
            method = "PUT"
            service = "s3"
            host = self._get_host()
            content_type = "application/octet-stream"
            request_parameters = ""

            now = datetime.datetime.utcnow()
            amz_date = now.strftime("%Y%m%dT%H%M%SZ")
            date_stamp = now.strftime("%Y%m%d")

            payload_hash = hashlib.sha256(payload).hexdigest()

            canonical_headers = (
                f"host:{host}\n"
                f"x-amz-content-sha256:{payload_hash}\n"
                f"x-amz-date:{amz_date}\n"
            )
            signed_headers = "host;x-amz-content-sha256;x-amz-date"

            canonical_request = (
                f"{method}\n"
                f"{self._get_canonical_uri(s3_key)}\n"
                f"{request_parameters}\n"
                f"{canonical_headers}\n"
                f"{signed_headers}\n"
                f"{payload_hash}"
            )

            algorithm = "AWS4-HMAC-SHA256"
            credential_scope = f"{date_stamp}/{self.region}/{service}/aws4_request"
            string_to_sign = (
                f"{algorithm}\n"
                f"{amz_date}\n"
                f"{credential_scope}\n"
                f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
            )

            signing_key = self._get_signature_key(date_stamp)
            signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

            authorization_header = (
                f"{algorithm} "
                f"Credential={self.access_key}/{credential_scope}, "
                f"SignedHeaders={signed_headers}, "
                f"Signature={signature}"
            )

            headers = {
                "x-amz-date": amz_date,
                "x-amz-content-sha256": payload_hash,
                "Authorization": authorization_header,
                "Content-Type": content_type,
            }

            url = f"{self.endpoint_url}/{self.bucket_name}/{s3_key}"
            response = requests.put(url, data=payload, headers=headers)

            if response.status_code in [200, 204]:
                logger.info(f"File uploaded: {s3_key}")
                return url if is_public else f"s3://{self.bucket_name}/{s3_key}"
            else:
                raise Exception(f"Upload failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Error uploading file to Contabo: {e}")
            raise

    def generate_presigned_url(self, s3_key, expires_in=3600):
        import boto3  # Import here to avoid unnecessary dependency if not used
        try:
            client = boto3.client(
                "s3",
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )

            url = client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": s3_key},
                ExpiresIn=expires_in,
            )
            logger.info(f"Generated presigned URL for: {s3_key}")
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {e}")
            raise

    def delete_file(self, s3_key):
        import boto3
        try:
            client = boto3.client(
                "s3",
                endpoint_url=self.endpoint_url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            )
            client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            logger.info(f"File deleted: {s3_key}")
            return f"File {s3_key} deleted successfully."
        except Exception as e:
            logger.error(f"Error deleting file from Contabo: {e}")
            raise

    def get_bucket_and_s3_key(self, s3_url):
        parsed_url = urlparse(s3_url)
        bucket = parsed_url.netloc
        key = parsed_url.path.lstrip("/")
        return bucket, key
