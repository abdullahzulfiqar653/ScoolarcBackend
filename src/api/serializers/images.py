from rest_framework import serializers
from botocore.exceptions import NoCredentialsError
from api.services.digital_ocean_s3 import S3Service

s3_client = S3Service()


class ImagesSerializer(serializers.Serializer):
    file = serializers.ImageField(write_only=True)
    public = serializers.BooleanField(default=False, write_only=True)
    presigned_url = serializers.URLField(read_only=True)

    def create(self, validated_data):
        request = self.context.get("request")
        file = validated_data.get("file")
        file_name = file.name.replace(" ", "_")
        is_public = validated_data.get("public", False)
        access_folder = "public" if is_public else "private"
        s3_key = f"{access_folder}/{request.merchant.id}/{file_name}"

        try:
            presigned_url = s3_client.upload_file(file, s3_key, is_public=is_public)
            return {"presigned_url": presigned_url}
        except NoCredentialsError:
            raise serializers.ValidationError(
                "AWS credentials are not configured correctly."
            )
        except Exception as e:
            raise serializers.ValidationError(f"Error uploading file: {str(e)}")
