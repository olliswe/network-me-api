from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from accounts.models import User, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name', 'organization','date_added', 'password', 'category')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        # category = Category.objects.get(name=validated_data.pop('category'))
        # user.category =
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.category = validated_data.get('category',instance.category)
        instance.save()
        return instance


