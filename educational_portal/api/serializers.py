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

class FacultiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculties
        fields = ('__all__')