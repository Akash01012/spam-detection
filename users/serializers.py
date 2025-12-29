from rest_framework import serializers
from .models import User, Contact, SpamMark, GlobalContact


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'phone_number', 'email']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email'),
        )
        user.set_password(validated_data['password'])  # 🔥 CRITICAL LINE
        user.save()
        return user
class ContactSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.IntegerField(source="global_contact.spam_likelihood", read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'email', 'spam_likelihood']


class GlobalContactSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.IntegerField(read_only=True)

    class Meta:
        model = GlobalContact
        fields = ['name', 'phone_number', 'email', 'spam_likelihood']


class SpamMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamMark
        fields = ['id', 'phone_number', 'marked_at']

    def create(self, validated_data):
        validated_data['marked_by'] = self.context['request'].user
        return super().create(validated_data)
