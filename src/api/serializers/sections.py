from rest_framework import serializers
from api.models.sections import Sections
from api.models import Subject
from api.serializers import StaffSerializer
from api.serializers import SubjectSerializer


class SectionsSerializer(serializers.ModelSerializer):
    coordinator = StaffSerializer(read_only=True)
    books = SubjectSerializer(many=True, read_only=True)
    books_ids = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=True, write_only=True, source='books'
    )

    class Meta:
        model = Sections
        fields = ['id', 'name', 'code', 'coordinator', 'books', 'books_ids', 'section_class', 'created_at', 'updated_at']

    def create(self, validated_data):
        books = validated_data.pop('books', [])
        section = Sections.objects.create(**validated_data)
        section.books.set(books)
        return section
