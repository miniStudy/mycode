from rest_framework import serializers  
from adminside.models import *


class BoardsSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Boards  
        fields = ('__all__') 

class stdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Std
        fields = ('__all__')

class subjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('__all__')

class chapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chepter
        fields = ('__all__')

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chepterwise_material
        fields = ('__all__')

class FacultiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculties
        fields = ('__all__')

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batches
        fields = ('__all__')

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcements
        fields = ('__all__')

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ('__all__')

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packs
        fields = ('__all__')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ('__all__')

class InquiriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiries
        fields = ('__all__')

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminData
        fields = ('__all__')

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ('__all__')

class Cheque_Collection_serial(serializers.ModelSerializer):
    class Meta:
        model = Cheque_Collection
        fields = ('__all__')

class Fees_Collection_serial(serializers.ModelSerializer):
    class Meta:
        model = Fees_Collection
        fields = ('__all__')

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('__all__')

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = ('__all__')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('__all__')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Image
        fields = ('__all__')

class DoubtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doubt_section
        fields = ('__all__')

class Test_attemted_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Test_attempted_users
        fields = ('__all__')










