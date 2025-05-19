from rest_framework.generics import CreateAPIView

from api.permissions import isMerchantMember
from api.serializers.images import ImagesSerializer

from drf_spectacular.utils import extend_schema


@extend_schema(
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "format": "binary"},  # Fix for file upload
                "public": {"type": "boolean"},
            },
            "required": ["file"],
        }
    },
    responses={200: ImagesSerializer},
)
class ImagesCreateAPIView(CreateAPIView):
    """

    **Request:**
    - Accepts the following **body parameters**:

      | Parameter | Required | Description |
      |-----------|--------  | -------------|
      | file    | ✅ Yes   | The file that will be uploaded. |
      | public  | ❌ No    | If true, the file will be publicly accessible. Default is False. |

    **Headers:**
    - Authorization: Token your_auth_token *(Required)*

    **Response:**
    - Returns a **pre-signed URL** that the client can use to upload the file directly to S3.
    """

    serializer_class = ImagesSerializer
    permission_classes = [isMerchantMember]
