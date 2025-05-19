from api.permissions import IsOutletMember, RolePermission
from api.serializers.student import StudentSerializer
from api.models.student import Student

from rest_framework import filters
from rest_framework.generics import ListCreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiExample


class OutletStudentListCreateAPIView(ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsOutletMember, RolePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ["address", "city", "primary_phone", "first_name", "area", "email"]

    def get_queryset(self):
        return Student.objects.filter(outlets=self.request.outlet)

    @extend_schema(
        description="""
**Request:**
- Accepts the following **body parameters** (all fields marked ✅ are required):

| Parameter         | Type     | Required | Notes                                                             |
|------------------|----------|----------|-------------------------------------------------------------------|
| city             | string   | ✅ Yes   | Cannot be blank                                                   |
| area             | string   | ✅ Yes   | Cannot be blank                                                   |
| gender           | string   | ✅ Yes   | "Male", "Female", or "Other"                                      |
| first_name       | string   | ✅ Yes   | Cannot be blank                                                   |
| last_name        | string   | ❌ No    | If provided, cannot be blank                                      |
| father_name      | string   | ✅ Yes   | Cannot be blank                                                   |
| mother_name      | string   | ✅ Yes   | Cannot be blank                                                   |
| father_cnic      | string   | ✅ Yes   | Cannot be blank                                                   |
| b_form[Image Url]| string   | ❌ No    | Send `null` if not applicable, empty string not allowed           |
| date_of_birth    | string   | ✅ Yes   | Format: YYYY-MM-DD                                                |
| blood_group      | string   | ❌ No    | If provided, cannot be blank                                      |
| address          | string   | ❌ No    | If provided, cannot be blank    
| religion         | string   | ❌ No    | If provided, cannot be blank                                      |
| student_section  | string   | ✅ Yes   | Must be a valid Section ID (PK), not null                         |
| student_guardian | object   | ✅ Yes   | Nested guardian object (see below)                                |

**Nested `student_guardian` object:**

| Field                  | Type     | Required | Notes                                     |
|------------------------|----------|----------|-------------------------------------------|
| city                   | string   | ✅ Yes   | Cannot be blank                           |
| area                   | string   | ✅ Yes   | Cannot be blank                           |
| gender                 | string   | ✅ Yes   | "Male", "Female", or "Other"              |
| occupation             | string   | ✅ Yes   | Cannot be blank                           |
| first_name             | string   | ✅ Yes   | Cannot be blank                           |
| blood_group            | string   | ❌ No    | If provided, cannot be blank              |
| primary_phone          | string   | ✅ Yes   | exact 10 digits like 3454545653           |
| emergency_contact      | string   | ❌ No    | exact 10 digits like 3454545653           |
| emergency_contact_name | string   | ❌ No    | If provided, cannot be blank              |
| email                  | string   | ❌ No    | Must be valid email format if provided    |
| cnic                   | string   | ✅ Yes   | exact 13 digits like 313033059281         |
| address                | string   | ❌ No    | If provided, cannot be blank              |
| religion               | string   | ❌ No    | If provided, cannot be blank              |
| date_of_birth          | string   | ❌ No    | Format: YYYY-MM-DD                        |

**Validation Notes:**
- Fields marked as ❌ Optional will still raise validation errors if passed as empty string `""`. Use `null` instead.
- `student_guardian` is a nested object, not just a primary key.
- `student_section` must reference an existing Section record (validated via PK).

**Headers:**
- Authorization: Token your_auth_token *(Required)*

**Response:**
- On success: returns the created student record.
- On error: returns validation errors for missing/blank/invalid fields.
        """,
        examples=[
            OpenApiExample(
                name="Complete Student Create Payload",
                value={
                    "city": "Rahim yar khan",
                    "area": "Gulshan Iqbal",
                    "avatar": "https://cdn.example.com/imgs/avatar.png",
                    "gender": "Male",
                    "b_form": "https://cdn.example.com/docs/bform.pdf",
                    "address": "House 123, Block A",
                    "last_name": "Khan",
                    "first_name": "Ali",
                    "blood_group": "O+",
                    "father_name": "Ahmed",
                    "mother_name": "Sara",
                    "father_cnic": "4210112345671",
                    "date_of_birth": "2025-04-20",
                    "student_section": "108sdzhv8wcjhb",  # replace with real PK
                    "religion": "Islam",
                    "student_guardian": {
                        "city": "Karachi",
                        "area": "DHA",
                        "cnic": "4210112345671",
                        "email": "guardian@example.com",
                        "avatar": "https://cdn.example.com/imgs/guardian-avatar.png",
                        "gender": "Male",
                        "religion": "Islam",
                        "address": "Flat 202, Sunset Towers",
                        "occupation": "Engineer",
                        "first_name": "Hamid",
                        "blood_group": "B+",
                        "primary_phone": "3001234567",
                        "date_of_birth": "1980-12-05",
                        "emergency_contact": "3012345678",
                        "emergency_contact_name": "Adeel",
                    },
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Success Response Example",
                value={
                    "count": 8,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": "109ERuX8QhsPQWd",
                            "city": "string",
                            "area": "string",
                            "role": "",
                            "avatar": "string",
                            "gender": "string",
                            "b_form": "string",
                            "address": "string",
                            "religion": "",
                            "last_name": "string",
                            "first_name": "Hahahaha",
                            "blood_group": "str",
                            "father_name": "string",
                            "mother_name": "string",
                            "father_cnic": "string",
                            "roll_number": "0001",
                            "date_of_birth": "2025-04-21",
                            "student_section": {
                                "id": "1081bba33ee9ae9",
                                "name": "testing section",
                                "code": "",
                                "section_class": {
                                    "id": "106vdfXJxPhL42a",
                                    "name": "updated class name",
                                },
                            },
                            "student_guardian": "1125v6Xnwfw6svm",
                        }
                    ],
                },
                response_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(
        description="""
**Retrieve all students linked to the current outlet.**

### 🔐 Headers
- `Authorization`: Token your_auth_token *(Required)*

### 🔎 Filters Supported:
- `search`: You can search using `first_name`, `last_name`, `primary_phone`, `email`, `area`, `address`.

### 📄 Response
- Returns a list of student records""",
        examples=[
            OpenApiExample(
                name="Success Response Example",
                value={
                    "id": "109ERuX8QhsPQWd",
                    "city": "string",
                    "area": "string",
                    "role": "",
                    "avatar": "string",
                    "gender": "string",
                    "b_form": "string",
                    "address": "string",
                    "religion": "",
                    "last_name": "string",
                    "first_name": "Hahahaha",
                    "blood_group": "str",
                    "father_name": "string",
                    "mother_name": "string",
                    "father_cnic": "string",
                    "roll_number": "0001",
                    "date_of_birth": "2025-04-21",
                    "student_section": {
                        "id": "1081bba33ee9ae9",
                        "name": "testing section",
                        "code": "",
                        "section_class": {
                            "id": "106vdfXJxPhL42a",
                            "name": "updated class name",
                        },
                    },
                    "student_guardian": "1125v6Xnwfw6svm",
                },
                response_only=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
