from rest_framework import serializers
from .models import AppUser
 
 
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = AppUser
        fields = ('id', 'email', 'username', 'password','first_name',
            'last_name', 'date_joined', 'age')
        read_only_fields = ('date_joined',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        instance = self.Meta.model.objects.create_user(**validated_data)
        return instance