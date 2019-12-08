from django.contrib.auth.models import User
from dashboard_app.models import Query, Answer
from rest_framework import serializers


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]

    def save(self):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        if password != "":
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError({'password': 'Password field cant be empty'})


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class QuerySerializers(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = [
            'question'
        ]

    def save(self, user):
        query = Query(
            question=self.validated_data['question'],
            asked_by=user
        )
        query.save()


class AnswerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'reply'
        ]
