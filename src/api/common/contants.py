MODEL_CODES = {
    "Lookup": "100",
    "OTP": "101",
    "Merchant": "102",
    "Outlet": "103",
    "Member": "104",
    "MerchantConfig": "105",
    "Classes": "106",
    "Staff": "107",
    "Section": "108",
    "Student": "109",
    "Subject": "110",
    "Invoice": "111",
    "Guardian": "112",
    "TransactionHistory": "113",
    "SectionStaffAndSubject": "114",
    "Attendance": "115",
}

STAFF = "staff"
PARENT = "parent"
STUDENT = "student"
TEACHER = "teacher"
MERCHANT = "merchant"
PRINCIPLE = "principal"
REGISTRAR = "registrar"

STAFF_ROLES = [PRINCIPLE, REGISTRAR, TEACHER]
ROLES_NOT_ALLOWED_TO_HAVE_PERMISSIONS = [STUDENT, PARENT]
ROLES_ALLOWED_TO_ASSIGN_PERMISSIONS = [MERCHANT, PRINCIPLE, REGISTRAR]

SMS = "sms"
EMAIL = "email"
WHATSAPP = "whatsapp"


ROLE_BASED_PERMISSIONS = {
    MERCHANT: [
        "api.add_classes",
        "api.change_classes",
        "api.delete_classes",
        "api.view_classes",
        "api.add_guardian",
        "api.change_guardian",
        "api.delete_guardian",
        "api.view_guardian",
        "api.add_invoice",
        "api.change_invoice",
        "api.view_invoice",
        "api.add_member",
        "api.change_member",
        "api.delete_member",
        "api.view_member",
        "api.add_merchantconfig",
        "api.change_merchantconfig",
        "api.delete_merchantconfig",
        "api.view_merchantconfig",
        "api.add_outlet",
        "api.change_outlet",
        "api.delete_outlet",
        "api.view_outlet",
        "api.add_section",
        "api.change_section",
        "api.delete_section",
        "api.view_section",
        "api.add_staff",
        "api.change_staff",
        "api.delete_staff",
        "api.view_staff",
        "api.add_sectionstaffandsubject",
        "api.change_sectionstaffandsubject",
        "api.delete_sectionstaffandsubject",
        "api.view_sectionstaffandsubject",
        "api.add_student",
        "api.change_student",
        "api.delete_student",
        "api.view_student",
        "api.add_subject",
        "api.change_subject",
        "api.delete_subject",
        "api.view_subject",
        "api.add_transactionhistory",
        "api.change_transactionhistory",
        "api.view_transactionhistory",
        "auth.add_permission",
        "auth.view_permission",
    ]
}
