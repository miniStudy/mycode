from rest_framework import serializers  
from adminside.models import *

class AdminDataSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = AdminData  
        fields = ('__all__') 

class BoardsSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = Boards  
        fields = ('__all__') 
